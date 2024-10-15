#!/usr/bin/python3

import sys
import src.algo.xor as xor
import src.algo.rsa as rsa
import src.algo.pgp_xor as pgp_xor

def parse_arguments():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    crypto_system = sys.argv[1]
    mode = sys.argv[2]

    if crypto_system not in ['xor', 'aes', 'rsa', 'pgp-xor', 'pgp-aes']:
        print(f"Erreur : CRYPTO_SYSTEM '{crypto_system}' non valide.")
        print_usage()
        sys.exit(1)

    if mode not in ['-c', '-d', '-g']:
        print(f"Erreur : MODE '{mode}' non valide.")
        print_usage()
        sys.exit(84)
    
    if mode == '-g':
        return {
            'CRYPTO_SYSTEM': crypto_system,
            'MODE': mode,
            'OPTIONS': {
                'block_mode': False,
                'P': sys.argv[3],
                'Q': sys.argv[4]
            }
        }
        

    use_block = False
    key = None

    for arg in sys.argv[3:]:
        if arg == '-b':
            use_block = True
        elif key is None:
            key = arg

    if mode in ['-c', '-d'] and key is None:
        print("Erreur : Une clé est requise pour les modes -c et -d.")
        print_usage()
        sys.exit(84)

    return {
        'CRYPTO_SYSTEM': crypto_system,
        'MODE': mode,
        'OPTIONS': {
            'block_mode': use_block,
            'key': key
        }
    }

def print_usage():
    print("Usage: my_pgp CRYPTO_SYSTEM MODE [OPTIONS] [key]")
    print("CRYPTO_SYSTEM:")
    print("  xor    : computation using XOR algorithm")
    print("  aes    : computation using 128-bit AES algorithm")
    print("  rsa    : computation using RSA algorithm")
    print("  pgp-xor: computation using both RSA and XOR algorithm")
    print("  pgp-aes: computation using both RSA and 128-bit AES algorithm")
    print("MODE:")
    print("  -c    : Cipher the MESSAGE")
    print("  -d    : Decipher the MESSAGE")
    print("OPTIONS:")
    print("  -b    : Block mode, MESSAGE and key must be the same size")
    print("key     : Hexadecimal key used to cipher/decipher MESSAGE")

def choose_crypto_system(args, message):
    if args['CRYPTO_SYSTEM'] == 'xor':
        return xor.xor_encrypt_decrypt(message, args)
    elif args['CRYPTO_SYSTEM'] == 'aes':
        print("AES not implemented yet.")
        return None
    elif args['CRYPTO_SYSTEM'] == 'rsa':
        return rsa.rsa_encrypt_decrypt(message, args)
    elif args['CRYPTO_SYSTEM'] == 'pgp-xor':
        return pgp_xor.pgp_rsa_xor(message, args)
    elif args['CRYPTO_SYSTEM'] == 'pgp-aes':
        print("PGP-AES not implemented yet.")
        return None
    else:
        exit(1)  