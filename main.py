from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-realtime-preview"

@app.post("/voice")
async def voice_handler():
    response = VoiceResponse()

    response.say("Bună ziua! Imediat vă conectez la asistentul inteligent.")

    response.connect().stream(
        url=f"wss://api.openai.com/v1/realtime?model={MODEL}",
        bidirectional=True,
        parameters={"openai-api-key": OPENAI_API_KEY}
    )

    return PlainTextResponse(str(response), media_type="text/xml")
