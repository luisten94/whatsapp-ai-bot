from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_ai_reply(user_message: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("Falta OPENAI_API_KEY en el .env")

    clean_message = (user_message or "").strip()
    if not clean_message:
        return "No recibí texto para responder."

    
    response = client.responses.create(
    model=OPENAI_MODEL,
    input=[
        {
            "role": "system",
            "content": (
                "Eres el asistente de ventas por WhatsApp de una tienda. "
                "Responde siempre en español. "
                "Sé breve, claro y amable. "
                "Ayuda al cliente a encontrar productos y resolver dudas. "
                "No inventes precios, stock, horarios ni políticas. "
                "Si no tienes esa información, indícalo claramente. "
                "Haz preguntas cortas para entender mejor lo que necesita el cliente."
            ),
        },
        {
            "role": "user",
            "content": clean_message,
        },
    ],
    )   

    text = (response.output_text or "").strip()

    if not text:
        return "No pude generar una respuesta en este momento."

    return text