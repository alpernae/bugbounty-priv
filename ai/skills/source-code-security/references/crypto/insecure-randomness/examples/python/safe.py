import secrets
import time

def create_password_reset_token(user_id: str) -> str:
    random_part = secrets.token_urlsafe(32)
    timestamp = int(time.time())
    return f"{user_id}.{timestamp}.{random_part}"
