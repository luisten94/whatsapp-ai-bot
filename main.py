from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from app.config import VERIFY_TOKEN
from app.normalize import parse_whatsapp_messages
from app.whatsapp import send_whatsapp_text
from app.logic import build_reply

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge or "")

    raise HTTPException(status_code=403, detail="Invalid verify token")

@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    messages = parse_whatsapp_messages(body)

    for msg in messages:
        if msg["type"] == "text" and msg["text"]:
            try:
                reply = await build_reply(msg["text"])
                await send_whatsapp_text(to=msg["from"], message=reply)
            except Exception as e:
                print("=== ERROR SENDING WHATSAPP MESSAGE ===")
                print(str(e))

    return JSONResponse({"status": "ok", "messages": messages})

@app.get("/test-reply")
async def test_reply():
    text = "Hola"
    reply = build_reply(text)
    return {'input': text, 'reply': reply}
