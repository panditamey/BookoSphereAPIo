from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

from features.generate import generate

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Input(BaseModel):
    prompt : str
    user : str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/generatebook')
async def generate_book(input:Input):
    print(input.user)
    try:
        pdf, audio, summary, bookName, imagecid_url = generate(input.prompt, input.user)
    except:
        return {"status": "failed"}
    return {
        "status": "success",
        "prompt": input.prompt,
        "pdf": pdf,
        "audio": audio,
        "description": summary,
        "name":bookName,
        "poster":imagecid_url
    }

@app.get("/model/{model}", response_class=HTMLResponse)
async def get_model(request: Request, model: str):
    return templates.TemplateResponse("index.html",
        {
            "request": request, 
            "model": model+".glb"
        }
)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
