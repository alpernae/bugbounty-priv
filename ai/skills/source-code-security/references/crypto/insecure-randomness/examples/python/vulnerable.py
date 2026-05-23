import random
import time

def create_password_reset_token(user_id: str) -> str:
    suffix = random.randint(0, 999999)
    timestamp = int(time.time())
    return f"{user_id}.{timestamp}.{suffix:06d}"
