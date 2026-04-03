from ai import generate_ai_reply


def build_reply(text: str) -> str:
    clean_text = (text or "").strip()

    if not clean_text:
        return "No recibí texto en tu mensaje."

    try:
        return generate_ai_reply(clean_text)
    except Exception as e:
        print(f"[build_reply] OpenAI error: {e}")
        return "Tuve un problema generando la respuesta. Intenta de nuevo en un momento."