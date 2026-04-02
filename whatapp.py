import httpx
from config import WHATSAPP_TOKEN, PHONE_NUMBER_ID, GRAPH_API_VERSION

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