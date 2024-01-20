from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from pydantic import BaseModel
import uvicorn


from generate import generate

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 


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

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)