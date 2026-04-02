from app.services.inventory_service import find_in_stock_product_by_name


async def build_reply(user_text: str) -> str:
    text = (user_text or "").strip().lower()

    if any(word in text for word in ["asesor", "humano", "persona", "agente", "soporte"]):
        return "Claro, puedo ayudarte a pasar con una persona. Cuéntame tu nombre y el motivo de tu consulta."

    if any(word in text for word in ["hola", "buenas", "hello"]):
        return "Hola. Te ayudo con productos, stock o pedidos. Si prefieres, también puedo pasarte con una persona."

    if any(word in text for word in ["stock", "disponible", "disponibilidad"]):
        product = await find_in_stock_product_by_name(user_text)
        if product:
            return (
                f"Sí, tenemos {product['name']} disponible. "
                f"Precio: {product.get('price', 'N/D')}. "
                f"Stock: {product.get('stock', 'N/D')}."
            )
        return f"Lo siento, no encontré el producto '{user_text}' en stock."

    if any(word in text for word in ["producto", "productos", "catalogo", "catálogo"]):
        return "Puedo ayudarte a buscar productos. Dime qué estás buscando."

    if any(word in text for word in ["pedido", "orden"]):
        return "Pásame tu número de pedido y te ayudo a revisarlo."

    if text == "menu":
        return "Puedo ayudarte con productos, stock, pedidos o pasarte con una persona."

    return f"Entiendo. Me escribiste: {user_text}. ¿Buscas un producto, revisar stock, un pedido o hablar con una persona?"

""" def build_reply(user_text: str) -> str:
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

    return f"Entiendo. Me escribiste: {user_text}. ¿Buscas un producto, revisar stock, un pedido o hablar con una persona?" ###
    
    """