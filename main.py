from fastapi import FastAPI, WebSocket
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os
import websockets
import asyncio

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-realtime-preview"


@app.post("/voice")
async def voice_handler():
    """Twilio entry point — generates TwiML."""
    response = VoiceResponse()
    response.say("Bună ziua! Un moment, vă conectez la asistentul inteligent.")
    response.connect().stream(url="wss://clinic-ai-realtime-backend.onrender.com/ws", bidirectional=True)
    return PlainTextResponse(str(response), media_type="text/xml")


@app.websocket("/ws")
async def websocket_proxy(ws: WebSocket):
    """Proxy WebSocket between Twilio <-> OpenAI Realtime"""
    await ws.accept()

    # Conectează la OpenAI Realtime
    async with websockets.connect(
        f"wss://api.openai.com/v1/realtime?model={MODEL}",
        extra_headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
    ) as openai_ws:

        async def from_twilio():
            async for msg in ws.iter_bytes():
                await openai_ws.send(msg)

        async def from_openai():
            async for msg in openai_ws:
                await ws.send_bytes(msg)

        await asyncio.gather(from_twilio(), from_openai())
