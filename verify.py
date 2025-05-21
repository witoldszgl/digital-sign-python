from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA3_256

with open("out/public.pem",      "rb") as f: pub_key_data = f.read()
with open("out/message_A.bin",   "rb") as f: message       = f.read()
with open("out/signature.sig",   "rb") as f: signature     = f.read()

pub_key = RSA.import_key(pub_key_data)

h = SHA3_256.new(message)

try:
    pkcs1_15.new(pub_key).verify(h, signature)
    print("Signature is VALID")
except (ValueError, TypeError):
    print("Signature is INVALID")
