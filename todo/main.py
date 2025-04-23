import os
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, task, authentication, explainer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
import requests
from fastapi.responses import FileResponse
import uvicorn
from typing import Optional


from google.oauth2 import id_token
from google.auth.transport import requests as grequest
from supabase import create_client, Client

app = FastAPI(
    title="TODO APP"
)
models.Base.metadata.create_all(engine)

app.include_router(explainer.router)
app.include_router(task.router)
app.include_router(user.router)
app.include_router(authentication.router)


origins = [
    "http://localhost:3000",
]

app.add_middleware(SessionMiddleware ,secret_key='maihoonjiyan')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=500
)


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Store connected clients
active_connections = set()

# data = {
#     "pipelineTasks": [
#         {
#             "taskType": "translation",
#             "config": {
#                 "language": {
#                     "sourceLanguage": "en",
#                     "targetLanguage": "hi"
#                 },
#                 "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
#             }
#         }
#     ],
#     "inputData": {
#         "input": [{ "source": "hello world" }],
#         "audio": []
#     }
# }

# data = {
#     "input": "hello world",
# }

# @app.get("/auth") 
# def authentication(request: Request,token:str): 
#     try: 
#         # Specify the CLIENT_ID of the app that accesses the backend: 
#         user =id_token.verify_oauth2_token(token, requests.Request(), "116988546-2a283t6anvr0.apps.googleusercontent.com") 
  
#         request.session['user'] = dict({ 
#             "email" : user["email"]  
#         }) 
          
#         return user['name'] + ' Logged In successfully'
  
#     except ValueError: 
#         return "unauthorized"

API_URL = "https://anuvaad-backend.bhashini.co.in/v1/pipeline"

data = {
  "pipelineTasks": [
    {
      "taskType": "translation",
      "config": {
        "language": {
          "sourceLanguage": "en",
          "targetLanguage": "hi"
        },
        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
      }
    }
  ],
  "inputData": {
    "input": [
      {
        "source": "hello world"
      }
    ],
    "audio": []
  }
}
@app.post("/translate")
async def translate(request):
    response = requests.post(API_URL, data, headers={"Content-Type": "application/json"})
    return response.json()


@app.post("/generate_talking_video/")
async def generate_talking_video(text: str = "hello! how are you? i am your new teacher"):
    # image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image_path = './Elegant Redhead Portrait.jpeg'
    # audio_path = os.path.join(OUTPUT_FOLDER, "speech.wav")
    audio_path = './download.mp3'
    output_video_path = os.path.join('.', "talking_video.mp4")
    
    # Save the uploaded image
    # with open(image_path, "wb") as f:
    #     f.write(image.file.read())
    
    # Use Wav2Lip for lip-syncing (ensure Wav2Lip is installed and configured)
    command = f"python Wav2Lip/inference.py --checkpoint_path Wav2Lip/checkpoints/wav2lip_gan.pth --face {image_path} --audio {audio_path} --outfile {output_video_path}"
    os.system(command)
    
    return FileResponse(output_video_path, media_type="video/mp4", filename="talking_video.mp4")


@app.get("/auth")
def authentication(request: Request,token:str):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user =id_token.verify_oauth2_token(token, requests.Request(), "116988534719-0j3baq1jkp64v4ghen352a283t6anvr0.apps.googleusercontent.com")

        request.session['user'] = dict({
            "email" : user["email"] 
        })
        
        return user['name'] + ' Logged In successfully'

    except ValueError:
        return "unauthorized"

@app.get('/')
def check(request:Request):
    return "hi "+ str(request.session.get('user')['email'])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)