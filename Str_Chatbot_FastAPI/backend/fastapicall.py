import requests

def call_fastapi(messages, user_id=None, conversation_id=None):
    payload = {
        "messages": messages,
        "user_id": user_id,
        "conversation_id": conversation_id,
    }
    r = requests.post("http://127.0.0.1:8000/chat", json=payload, timeout=120)
    r.raise_for_status()
    # print(r.json())
    return r.json()
