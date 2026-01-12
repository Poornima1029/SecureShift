from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets
import os

# Fallback shared key (for backward compatibility)
SHARED_SECRET_KEY = b'0123456789ABCDEF0123456789ABCDEF'

def generate_fresh_aes_key():
    """Generate cryptographically secure 32-byte AES-256 key every time"""
    return secrets.token_bytes(32)

def encrypt_data(key, plaintext: str) -> bytes:
    """Encrypt with any 32-byte key"""
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv + ct

def decrypt_data(key, ciphertext: bytes) -> str:
    """Decrypt with matching key"""
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
    return pt.decode()
