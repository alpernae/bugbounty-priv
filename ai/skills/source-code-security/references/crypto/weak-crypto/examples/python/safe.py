from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_note(note: bytes, key: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("key must be 256 bits")
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, note, None)
    return nonce + ciphertext
