#!/usr/bin/python3

from math import gcd
from random import randrange
import src.utils.little_endian as little_endian

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        exit(84)
    else:
        return x % m

FERMAT_PRIMES = [65537, 257, 17, 5, 3]

def generate_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = None
    for fermat_prime in FERMAT_PRIMES:
        if 1 < fermat_prime < phi and gcd(fermat_prime, phi) == 1:
            e = fermat_prime
            break
    
    if e is None:
        exit(84)
    
    d = mod_inverse(e, phi)

    public_key = little_endian.to_little_endian_hex(e) + '-' + little_endian.to_little_endian_hex(n)
    private_key = little_endian.to_little_endian_hex(d) + '-' + little_endian.to_little_endian_hex(n)

    print(f"public key: {public_key}")
    print(f"private key: {private_key}")
    
    return public_key, private_key

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def rsa_encrypt_decrypt(message, args):

    if args['MODE'] == '-g':

        p = int(args['OPTIONS']['P'], 16)
        q = int(args['OPTIONS']['Q'], 16)
        print(q)
        print(p)
        if not is_prime(p) or not is_prime(q):
            print("Erreur: nombres pas premiers")
            exit(84)
        generate_key(p, q)

    elif args['MODE'] == '-c':
        public_key = tuple(int.from_bytes(bytes.fromhex(x)[::-1], byteorder='big') for x in args['OPTIONS']['key'].split('-'))
        e, n = public_key
    
        message_bytes = message.encode()[::-1]

        m = int.from_bytes(message_bytes, byteorder='big')

        c = pow(m, e, n)

        return little_endian.to_little_endian_hex(c)

    elif args['MODE'] == '-d':
        private_key = tuple(int.from_bytes(bytes.fromhex(x)[::-1], byteorder='big') for x in args['OPTIONS']['key'].split('-'))
        d, n = private_key

        cipher_bytes = bytes.fromhex(message)[::-1]

        c = int.from_bytes(cipher_bytes, byteorder='big')

        m = pow(c, d, n)

        decrypted_message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')

        return decrypted_message[::-1].decode('utf-8', errors='replace')
