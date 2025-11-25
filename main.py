from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os

app = FastAPI()

OPENAI_REALTIME_MODEL = "gpt-4o-realtime-preview"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/voice")
async def voice_handler(request: Request):
    """Twilio entry point when someone calls your number."""
    response = VoiceResponse()

    response.say("Bună ziua! Un moment, vă conectez la asistentul inteligent.")

    response.connect().stream(
        url=f"wss://api.openai.com/v1/realtime?model={OPENAI_REALTIME_MODEL}",
        bidirectional=True,
        parameters={
            "openai-api-key": OPENAI_API_KEY
        }
    )

    return PlainTextResponse(str(response), media_type="text/xml")
