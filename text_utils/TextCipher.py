import base64
from Crypto import Random
from Crypto.Cipher import AES
import hmac
import hashlib


class TextCipher:
    HMAC_SIZE = hashlib.sha256().digest_size
    HMAC_KEY = b"HMACKEY"

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, data):
        data = self._pad(data)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encoded_data = base64.b64encode(iv + cipher.encrypt(data))
        sig = hmac.new(self.HMAC_KEY, encoded_data, hashlib.sha256).digest()
        return encoded_data + sig

    def decrypt(self, enc):
        sig = enc[-self.HMAC_SIZE:]
        enc = enc[:-self.HMAC_SIZE]

        check_sig = hmac.new(self.HMAC_KEY, enc, hashlib.sha256).digest()
        if hmac.compare_digest(check_sig, sig):
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        else:
            return None

    def _pad(self, s):
        return bytes(s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs), "UTF-8")

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


