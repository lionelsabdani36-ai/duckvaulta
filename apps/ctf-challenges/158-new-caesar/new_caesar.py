#!/usr/bin/env python3
"""new_caesar.py - Challenge #158 New Caesar (Cryptography, Medium).

Cipher custom dua lapis:
  1. Base16: tiap byte plaintext jadi 2 huruf (a=0 .. p=15).
  2. Additive key: tiap simbol digeser maju sejauh KEY_OFFSET (m = 12).
Contoh: encrypt("et_tu?_a91448ca") == "cbdabldadbplblcnpfpnpapapecpcn"
Tugas: analisis file ini, balikkan kedua lapis, dekripsi ciphertext.
"""

import string

ALPHABET = string.ascii_lowercase[:16]
OFF = ord('a')
KEY_OFFSET = 12  # huruf 'm'

def encrypt(plaintext):
    enc = ''
    for c in plaintext:
        binary = '{0:08b}'.format(ord(c))
        enc += ALPHABET[int(binary[:4], 2)]
        enc += ALPHABET[int(binary[4:], 2)]
    keyed = ''
    for c in enc:
        keyed += ALPHABET[((ord(c) - OFF) + KEY_OFFSET) % 16]
    return keyed

if __name__ == '__main__':
    print(encrypt('et_tu?_a91448ca'))
