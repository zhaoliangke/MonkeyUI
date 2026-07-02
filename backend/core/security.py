import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from django.conf import settings


def _get_aes_key():
    key = settings.AES_SECRET_KEY.encode('utf-8')
    if len(key) < 32:
        key = key.ljust(32, b'0')
    return key[:32]


def aes_encrypt(plain_text: str) -> str:
    if not plain_text:
        return ''
    key = _get_aes_key()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode('utf-8')


def aes_decrypt(cipher_text: str) -> str:
    if not cipher_text:
        return ''
    key = _get_aes_key()
    raw = base64.b64decode(cipher_text)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode('utf-8')


def mask_string(value: str, show_start: int = 2, show_end: int = 2) -> str:
    if not value:
        return ''
    if len(value) <= show_start + show_end:
        return '*' * len(value)
    return value[:show_start] + '*' * (len(value) - show_start - show_end) + value[-show_end:]
