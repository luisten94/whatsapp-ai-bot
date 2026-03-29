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