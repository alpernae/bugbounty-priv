import hashlib
from Crypto.Cipher import DES3

def encrypt_note(note: bytes, password: str) -> bytes:
    key = hashlib.md5(password.encode()).digest()
    cipher = DES3.new(key + key[:8], DES3.MODE_ECB)
    padded = note + b" " * (8 - len(note) % 8)
    return cipher.encrypt(padded)
