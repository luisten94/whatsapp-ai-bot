import os
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "luis123")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v25.0")


def parse_whatsapp_messages(body: dict) -> list[dict]:
    normalized_messages = []

    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])

            for msg in messages:
                from_number = msg.get("from")
                msg_type = msg.get("type")
                text = None

                if msg_type == "text":
                    text = msg.get("text", {}).get("body", "")

                normalized_messages.append({
                    "channel": "whatsapp",
                    "from": from_number,
                    "type": msg_type,
                    "text": text,
                    "message_id": msg.get("id"),
                    "timestamp": msg.get("timestamp"),
                })

    return normalized_messages


async def send_whatsapp_text(to: str, message: str):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        raise RuntimeError("Faltan WHATSAPP_TOKEN o PHONE_NUMBER_ID")

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message},
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        print("=== SEND RESPONSE STATUS ===")
        print(response.status_code)
        print(response.text)
        response.raise_for_status()


def build_reply(user_text: str) -> str:
    text = (user_text or "").strip().lower()

    if any(word in text for word in ["asesor", "humano", "persona", "agente", "soporte"]):
        return "Claro, puedo ayudarte a pasar con una persona. Cuéntame tu nombre y el motivo de tu consulta."

    if any(word in text for word in ["hola", "buenas", "hello"]):
        return "Hola. Te ayudo con productos, stock o pedidos. Si prefieres, también puedo pasarte con una persona."

    if any(word in text for word in ["producto", "productos", "catalogo", "catálogo"]):
        return "Puedo ayudarte a buscar productos. Dime qué estás buscando."

    if any(word in text for word in ["stock", "disponible", "disponibilidad"]):
        return "Claro. Dime el nombre del producto y te reviso disponibilidad."

    if any(word in text for word in ["pedido", "orden"]):
        return "Pásame tu número de pedido y te ayudo a revisarlo."

    if text == "menu":
        return "Puedo ayudarte con productos, stock, pedidos o pasarte con una persona."

    return f"Entiendo. Me escribiste: {user_text}. ¿Buscas un producto, revisar stock, un pedido o hablar con una persona?"


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

    print("=== WEBHOOK EVENT ===")
    print(body)

    messages = parse_whatsapp_messages(body)

    print("=== NORMALIZED MESSAGES ===")
    print(messages)

    for msg in messages:
        if msg["type"] == "text" and msg["text"]:
            try:
                reply = build_reply(msg["text"])
                await send_whatsapp_text(to=msg["from"], message=reply)
            except Exception as e:
                print("=== ERROR SENDING WHATSAPP MESSAGE ===")
                print(str(e))

    return JSONResponse({
        "status": "ok",
        "messages": messages
    })