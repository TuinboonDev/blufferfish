from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa

class Encryption:
    def create_cipher(self, shared_secret):
        self.cipher = Cipher(algorithms.AES(shared_secret),
                        modes.CFB8(shared_secret),
                        backend=default_backend())

    def get_cipher(self):
        return self.cipher

    def encrypt(self, data):
        return self.cipher.encryptor().update(data)

    def decrypt(self, data):
        return self.cipher.decryptor().update(data)

    def gen_keys(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024, backend=default_backend())

        self.public_key = self.private_key.public_key().public_bytes(encoding=serialization.Encoding.DER,
                                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key
