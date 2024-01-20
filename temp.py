import requests
import firebase_admin
from firebase_admin import credentials, storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'storageBucket': 'bookosphereapp.appspot.com'}) 


# API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content
image_bytes = query({
    "inputs": "Life of King Kalia of Dark Kingdom named Nalasopara.",
})
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))
image.save("asdf.jpg")
bucket = storage.bucket()
blob = bucket.blob("asdf"+".jpg")
blob.upload_from_string(image_bytes, content_type="image/jpeg")
blob.make_public()
imagecid_url = blob.public_url
print(f"Uploaded image URL : {imagecid_url}")