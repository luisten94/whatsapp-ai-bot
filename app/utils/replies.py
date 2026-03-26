def build_reply(user_text: str) -> str:
    text = (user_text or "").strip().lower()

    if any(word in text for word in ["asesor", "humano", "persona", "agente", "soporte"]):
        return "Claro, puedo ayudarte a pasar con una persona. Cuéntame tu nombre y el motivo de la consulta."

    if any(word in text for word in ["hola", "buenas"]):
        return "Hola. Te ayudo con productos, stock o pedidos. Si prefieres, también puedo pasarte con una persona."

    if any(word in text for word in ["producto", "productos", "catalogo", "catálogo"]):
        return "Puedo ayudarte a buscar productos. Dime qué estás buscando."

    if any(word in text for word in ["stock", "disponible", "disponibilidad"]):
        return "Claro. Dime el nombre del producto y te reviso disponibilidad."

    if any(word in text for word in ["pedido", "orden"]):
        return "Pásame tu número de pedido y te ayudo a revisarlo."

    return f"Entiendo. Me escribiste: {user_text}. ¿Buscas un producto, revisar stock, un pedido o hablar con una persona?"