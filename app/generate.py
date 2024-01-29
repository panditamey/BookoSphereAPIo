import datetime
import io
import os
import re
from fpdf import FPDF
import google.generativeai as genai
from dotenv import load_dotenv
from gtts import gTTS
import requests
import firebase_admin
from firebase_admin import credentials, storage , firestore
import io
from PIL import Image
from uuid import uuid4

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'bookosphereapp.appspot.com'}) 
db = firestore.client()
load_dotenv()

def generate(p,user):
    symbol_pattern = r'[^\w\s]' 
    genai.configure(api_key="AIzaSyAUfPsa_F6RlaXH3-z3Nkd46R8fFvYzu1o")

    palm = genai.GenerativeModel('gemini-pro')
    response =  palm.generate_content(p+"(write only text without any * # @ ! symbols))")
    text = re.sub(symbol_pattern, '', response.text)

    summary = palm.generate_content("Summarize in 20 words: "+text)
    summary = re.sub(symbol_pattern, '', summary.text)

    bookName = palm.generate_content("Give one book name for below book: "+text)
    bookName = re.sub(symbol_pattern, '', bookName.text)

    # API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    image_bytes = query({
        "inputs": summary,
    })
    # import io
    # from PIL import Image
    # image = Image.open(io.BytesIO(image_bytes))
    # image.save("asdf.jpg")
    bucket = storage.bucket()
    blob = bucket.blob(bookName+".jpg")
    blob.upload_from_string(image_bytes, content_type="image/jpeg")
    blob.make_public()
    imagecid_url = blob.public_url
    print(f"Uploaded image URL : {imagecid_url}")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)

    pdf.multi_cell(0, 10, txt=text)
    pdf_buffer = io.BytesIO()
    pdf_buffer.write(pdf.output(dest='S').encode('latin1'))
    pdf_buffer.seek(0)

    blob = bucket.blob(bookName+".pdf")
    blob.upload_from_string(pdf_buffer.getvalue(), content_type="application/pdf")
    blob.make_public()
    pdfcid_url = blob.public_url

    print(f"Uploaded PDF URL: {pdfcid_url}")


    myobj = gTTS(text=text, lang='en', slow=False)
    mp3_buffer = io.BytesIO()
    myobj.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)

    blob = bucket.blob(bookName+".mp3")
    blob.upload_from_string(mp3_buffer.getvalue(), content_type="audio/mp3")
    blob.make_public()
    audiocid_url = blob.public_url

    print(f"Uploaded audio URL: {audiocid_url}")

    doc_ref = db.collection(u'generatedbooks').document(str(uuid4()))
    doc_ref.set({
        u'name': bookName,
        u'bookURL': pdfcid_url,
        u'audioURL': audiocid_url,
        u'description': summary,
        u'posterURL': imagecid_url,
        u'public':False,
        u'author':user,
        u'rating':None,
        u'created_at': datetime.datetime.now()
    })

    return pdfcid_url, audiocid_url, summary, bookName, imagecid_url
    
