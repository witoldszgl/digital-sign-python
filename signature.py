from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA3_256
import os

def save_file(path: str, data: bytes):
    with open(path, "wb") as f:
        f.write(data)
    print(f"  • saved: {path}")

def main():
    os.makedirs("out", exist_ok=True)

    # --- 1) TRNG: get random seed and save it ---
    seed = get_random_bytes(32)
    save_file("out/trng_seed.bin", seed)

    # --- 2) RSA: generate private/public key pair using TRNG ---

    key = RSA.generate(2048, randfunc=get_random_bytes)
    priv_key = key
    pub_key = key.publickey()

    save_file("out/private.pem", priv_key.export_key(format="PEM"))
    save_file("out/public.pem", pub_key.export_key(format="PEM"))

    # --- 3) A: define the message and save it ---
    A = b"Test message"
    save_file("out/message_A.bin", A)

    # --- 4) A: compute SHA3-256 hash (#A) and save ---
    hash_A = SHA3_256.new(A)
    save_file("out/hash_A.bin", hash_A.digest())

    # --- 5) A: sign the hash with private key and save ---
    signature = pkcs1_15.new(priv_key).sign(hash_A)
    save_file("out/signature.sig", signature)

    # --- 6) B: read message, compute hash (#B) and save ---
    B = open("out/message_A.bin", "rb").read()
    hash_B = SHA3_256.new(B)
    save_file("out/hash_B.bin", hash_B.digest())

    # --- 7) B: verify signature using public key ---
    try:
        pkcs1_15.new(pub_key).verify(hash_B, signature)
        print("Verification: signature is valid")
    except (ValueError, TypeError):
        print("Verification: signature is invalid")

if __name__ == "__main__":
    main()
