from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

app = FastAPI()
COUNTER = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class UserSignup(BaseModel):
    username: str
    password: str
    input_type: str  # Expecting "audio" or "text"
    subcounty: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserMessage(BaseModel):
    message: str

class UserImage(BaseModel):
    image: str

class UserAudio(BaseModel):
   audio: str

class UserAudioImage(BaseModel):
   text: str

class UserUpdate(BaseModel):
    current_username: str
    new_username: Optional[str] = None
    new_password: Optional[str] = None
    input_type: Optional[str] = None
    subcounty: Optional[str] = None

@app.post("/signup")
async def signup(data: UserSignup,):
    return {"status": "success", "message": "User registered successfully"}

@app.post("/login")
def login(data: UserLogin):
    return {"status": "success", "message": "User registered successfully"}

@app.post("/message")
def handle_message(data: UserMessage):
    reply = handle_intent(data.message.lower())
    return {"reply": reply}

@app.post("/image")
def handle_image(data: UserImage):
    reply = "The following issues were identified in your crop: Issue: overwatering or drowning, Treatment: remove the crop from the field to salvage some"
    return {"reply": reply}

@app.post("/image_audio")
def handle_image_audio(data: UserAudioImage):
    return {"audio_url": f"/audio/{'download (1).wav'}"}

@app.post("/audio")
def handle_audio(data: UserAudio):
    global COUNTER
    print(COUNTER)

    if COUNTER == 0:
        reply = "I saw a sign at the farm that said 'Duck, eggs'. I was contemplating the use of the comma when it hit me."
        audio_filename = "download (2).wav"
    elif COUNTER == 1:
        reply = "Your expected harvest date is August 2nd 2026. With optimal conditions, you can expect a yeild of 1536 kilograms per hectare. The total amount of water you can expect to use is 5000 tonnes per hectare"
        audio_filename = "download.wav"
    elif COUNTER == 2:
        reply = "Please provide a crop image"
        audio_filename = "download (3).wav"
    
    COUNTER += 1
    return {"reply": reply, "audio_url": f"/audio/{audio_filename}"}

@app.post("/update_profile")
def update_profile(data: UserUpdate):
    return {
        "username": "hannah",
        "input_type": "text",
        "subcounty": "Bungoma",
    }

@app.get("/audio/{filename}")
def get_audio(filename: str, background_tasks: BackgroundTasks):
    audio_path = os.path.join(BASE_DIR, "data", filename)
    print("Audio path server: ", audio_path)

    if not os.path.isfile(audio_path):
        raise HTTPException(404, "Audio file not found")
    
    return FileResponse(audio_path, media_type="audio/wav", filename=filename)

def handle_intent(text):
    if "simulate" in text:
        reply = "Your expected harvest date is August 2nd 2026. With optimal conditions, you can expect a yeild of 1536 kilograms per hectare. The total amount of water you can expect to use is 5000 tonnes per hectare"
    elif "analyze" in text:
        reply = "Please provide an image"
    elif "hello" in text:
        reply = "Hello. How may I help you today?"
    elif "joke" in text:
        reply = "Why did the farmer become a great DJ? Because he knew when to drop the beets."
    else:
        reply = "Sorry. I didn't get that."

    return reply

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    print("Application started at port 8000")
