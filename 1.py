import base64
import hashlib
import hmac
from Crypto.Cipher import AES


def AES_Encrypt(data, client_id, secret):
    md5_iv = hashlib.md5(client_id).digest()
    md5_key = hashlib.md5(secret).digest()
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad(data)
    cipher = AES.new(md5_key, AES.MODE_CBC, md5_iv)
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    encodestrs = base64.b64encode(encryptedbytes)
    enctext = encodestrs.decode('utf8')
    return enctext

f = AES_Encrypt('12345678',bytes('e0c5660e0f9', encoding='utf-8'),bytes('fcbX26HEFHH5', encoding='utf-8'))
print(f)

