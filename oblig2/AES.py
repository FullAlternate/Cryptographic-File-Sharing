from Crypto import Random
from Crypto.Cipher import AES


class AES_Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s+b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size = 256):
        e_data = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        return iv + cipher.encrypt(e_data)

    def decrypt(self, cipher_text, key):
        iv = cipher_text[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        d_data = cipher.decrypt(cipher_text[AES.block_size:])

        return d_data.rstrip(b"\0")

