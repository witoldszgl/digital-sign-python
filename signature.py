from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA3_256
import os


def save_file(path: str, data: bytes):
    """Save bytes to a file, creating directories as needed."""
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  • saved: {path}")


def generate_keys(out_dir: str = "out"):
    """Generate RSA key pair and save to out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    seed = get_random_bytes(32)
    save_file(os.path.join(out_dir, "seed.bin"), seed)

    key = RSA.generate(2048, randfunc=get_random_bytes)
    save_file(os.path.join(out_dir, "private.pem"), key.export_key(format="PEM"))
    save_file(os.path.join(out_dir, "public.pem"), key.publickey().export_key(format="PEM"))
    return key, key.publickey()


def sign_file(file_path: str, priv_key: RSA.RsaKey):
    """Compute SHA3-256 hash of file and write a .sig signature alongside."""
    if not os.path.isfile(file_path):
        print(f"Error: plik '{file_path}' nie istnieje.")
        return
    data = open(file_path, "rb").read()
    h = SHA3_256.new(data)
    signature = pkcs1_15.new(priv_key).sign(h)
    sig_path = file_path + ".sig"
    save_file(sig_path, signature)
    print(f"Signed {file_path} -> {sig_path}")


def main():
    # Przygotuj katalog na klucze
    os.makedirs("out", exist_ok=True)
    key_path = os.path.join("out", "private.pem")
    pub_path = os.path.join("out", "public.pem")

    # Załaduj lub wygeneruj klucze
    if os.path.exists(key_path) and os.path.exists(pub_path):
        priv_key = RSA.import_key(open(key_path, 'rb').read())
        pub_key = RSA.import_key(open(pub_path, 'rb').read())
    else:
        priv_key, pub_key = generate_keys()

    # Wyświetl klucze w terminalu
    print("--- Private Key (PEM) ---")
    print(priv_key.export_key().decode())
    print("--- Public Key (PEM) ---")
    print(pub_key.export_key().decode())

    # Zapytaj użytkownika o plik do podpisu
    file_path = input("Podaj ścieżkę do pliku do podpisania: ")
    sign_file(file_path, priv_key)


if __name__ == "__main__":
    main()
