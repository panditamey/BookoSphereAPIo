from fastapi import FastAPI
from pydantic import BaseModel


from generate import generate

app = FastAPI()

class Input(BaseModel):
    prompt : str
    user : str

# class User(BaseModel):
#     user : str
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/generatebook')
async def generatebook(input:Input):
    print(input.user)
    try:
        pdf, audio, summary, bookName, imagecid_url = generate(input.prompt, input.user)
    except:
        return {"status": "failed"}

    # generate("Astronaut riding a horse")
    # palm.configure(api_key="AIzaSyAUfPsa_F6RlaXH3-z3Nkd46R8fFvYzu1o")
    # response = palm.generate_text(prompt="Write a book on india in 1000 words with 5 chapters.")
    # response = palm.generate_text(prompt=prompt.prompt)
    # text = response.result
    # print(response.result)
    return {
        "status": "success",
        "prompt": input.prompt,
        "pdf": pdf,
        "audio": audio,
        "description": summary,
        "name":bookName,
        "poster":imagecid_url
    }
    # return {"status": "success"}