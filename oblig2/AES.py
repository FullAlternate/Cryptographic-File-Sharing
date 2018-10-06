from Crypto import Random
from Crypto.Cipher import AES


class AES_Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):

        # Pads extra data to string making it a multiple of the cipher block size
        return s+b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key):

        e_data = self.pad(message)  # Pads message
        iv = Random.new().read(AES.block_size)  # Creates a random iv with same size as cipher block size
        cipher = AES.new(key, AES.MODE_CBC, iv)  # Generates a cipher object using key and iv

        return iv + cipher.encrypt(e_data)  # Encrypts and appends iv to data

    def decrypt(self, cipher_text, key):

        iv = cipher_text[:AES.block_size]   # Separates appended iv string from data
        cipher = AES.new(key, AES.MODE_CBC, iv)  # Generates a cipher object using key and iv
        d_data = cipher.decrypt(cipher_text[AES.block_size:])  # Decrypt data using the cipher object

        return d_data.rstrip(b"\0")  # Removes added padding and returns clean string

