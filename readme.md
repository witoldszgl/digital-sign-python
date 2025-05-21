# README / Instrukcja

## Opis / Description

Ten projekt pokazuje, jak generować i weryfikować podpis cyfrowy w Pythonie przy użyciu biblioteki PyCryptodome.

This project demonstrates how to generate and verify a digital signature in Python using the PyCryptodome library.

---

## Wymagania / Requirements

* Python 3.6 lub nowszy / Python 3.6+
* PyCryptodome (`pip install pycryptodome`)

---

## Struktura projektu / Project Structure

```
├── signature.py     # skrypt generujący klucze, skróty i podpis, a następnie weryfikujący
├── verify.py        # (opcjonalne) samodzielny skrypt do weryfikacji istniejących plików
└── out/             # katalog wyjściowy z wygenerowanymi plikami
    ├── trng_seed.bin
    ├── private.pem
    ├── public.pem
    ├── message_A.bin
    ├── hash_A.bin
    ├── signature.sig
    └── hash_B.bin
```

---

## Jak uruchomić / Usage

### Polski

1. Zainstaluj wymagane biblioteki:

   ```bash
   pip install pycryptodome
   ```
2. Uruchom główny skrypt:

   ```bash
   python signature.py
   ```
3. W katalogu `out/` znajdziesz wygenerowane pliki:

   * `trng_seed.bin`  – surowy ciąg losowy (TRNG)
   * `private.pem`    – klucz prywatny (PEM)
   * `public.pem`     – klucz publiczny (PEM)
   * `message_A.bin`  – podpisywana wiadomość
   * `hash_A.bin`     – skrót SHA3-256 wiadomości
   * `signature.sig`  – podpis RSA
   * `hash_B.bin`     – skrót tej samej wiadomości obliczony ponownie
4. (Opcjonalnie) Zweryfikuj podpis osobno:

   ```bash
   python verify.py
   ```

   lub za pomocą OpenSSL:

   ```bash
   openssl dgst -sha3-256 \
     -verify out/public.pem \
     -signature out/signature.sig \
     out/message_A.bin
   ```

### English

1. Install dependencies:

   ```bash
   pip install pycryptodome
   ```
2. Run the main script:

   ```bash
   python signature.py
   ```
3. Check the `out/` directory for generated files:

   * `trng_seed.bin`  – raw random seed (TRNG)
   * `private.pem`    – private RSA key (PEM)
   * `public.pem`     – public RSA key (PEM)
   * `message_A.bin`  – the message being signed
   * `hash_A.bin`     – SHA3-256 hash of the message
   * `signature.sig`  – RSA signature of the hash
   * `hash_B.bin`     – SHA3-256 hash recomputed by verifier
4. (Optional) Verify the signature separately:

   ```bash
   python verify.py
   ```

   or using OpenSSL:

   ```bash
   openssl dgst -sha3-256 \
     -verify out/public.pem \
     -signature out/signature.sig \
     out/message_A.bin
   ```
