# README / Instrukcja

## Opis / Description

Ten projekt pokazuje, jak generować klucze RSA, wyświetlać je, a następnie podpisywać dowolne pliki w Pythonie przy użyciu biblioteki PyCryptodome.

This project demonstrates how to generate an RSA key pair, display them, and then sign arbitrary files in Python using the PyCryptodome library.

---

## Wymagania / Requirements

* Python 3.6 lub nowszy / Python 3.6+
* PyCryptodome (`pip install pycryptodome`)

---

## Struktura projektu / Project Structure

```
├── signature.py     # główny skrypt do generowania kluczy, wyświetlania ich i podpisywania plików
├── README.md        # ta instrukcja
└── out/             # katalog wyjściowy na wygenerowane klucze i ziarnko TRNG
    ├── seed.bin
    ├── private.pem
    └── public.pem
```

---

## Jak uruchomić / Usage

### Polski

1. Zainstaluj wymagane biblioteki:

   ```bash
   pip install pycryptodome
   ```
2. Uruchom skrypt:

   ```bash
   python signature.py
   ```
3. Skrypt:

   1. Wygeneruje parę kluczy RSA (private.pem i public.pem) oraz plik `seed.bin` w katalogu `out/`, jeśli ich tam nie ma.
   2. Wyświetli w terminalu oba klucze w formacie PEM.
   3. Poprosi o podanie ścieżki do pliku, który chcesz podpisać.
   4. Utworzy plik z podpisem o tej samej nazwie z dopiskiem `.sig` obok oryginału.

### English

1. Install dependencies:

   ```bash
   pip install pycryptodome
   ```
2. Run the script:

   ```bash
   python signature.py
   ```
3. The script will:

   1. Generate an RSA key pair (`private.pem` and `public.pem`) and a raw TRNG seed file (`seed.bin`) in the `out/` directory if they do not already exist.
   2. Print both keys in PEM format to the console.
   3. Prompt you to enter the path to the file you want to sign.
   4. Create a signature file named `<original>.sig` next to the original file.

---

## Weryfikacja (opcjonalnie) / Verification (optional)

Aktualny skrypt nie zawiera osobnej weryfikacji, ale możesz użyć poniższego fragmentu lub biblioteki OpenSSL.

**Przykład w Pythonie:**

```python
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA3_256

# Załaduj klucz publiczny
pub_key = RSA.import_key(open('out/public.pem','rb').read())

def verify(file_path, sig_path):
    data = open(file_path,'rb').read()
    h = SHA3_256.new(data)
    sig = open(sig_path,'rb').read()
    try:
        pkcs1_15.new(pub_key).verify(h, sig)
        print('Signature valid')
    except (ValueError, TypeError):
        print('Signature invalid')

verify('ścieżka/do/pliku','ścieżka/do/pliku.sig')
```

**OpenSSL:**

```bash
openssl dgst -sha3-256 \
  -verify out/public.pem \
  -signature yourfile.ext.sig \
  yourfile.ext
```
