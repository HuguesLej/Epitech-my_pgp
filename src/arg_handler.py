#!/usr/bin/python3

import sys
import src.algo.xor as xor
import src.algo.rsa as rsa
import src.algo.pgp_xor as pgp_xor

def parse_arguments():
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("Erreur : Nombre d'arguments incorrect.")
        print_usage()
        sys.exit(84)

    crypto_system = sys.argv[1]
    mode = sys.argv[2]

    if crypto_system not in ['xor', 'aes', 'rsa', 'pgp-xor', 'pgp-aes']:
        print(f"Erreur : CRYPTO_SYSTEM '{crypto_system}' non valide.")
        print_usage()
        sys.exit(84)

    if mode not in ['-c', '-d', '-g']:
        print(f"Erreur : MODE '{mode}' non valide.")
        print_usage()
        sys.exit(84)
    
    if mode == '-g':

        if crypto_system != 'rsa':
            print("Erreur : Le mode -g n'est disponible que pour RSA.")
            print_usage()
            sys.exit(84)

        if len(sys.argv) != 5:
            print("Erreur : Le mode -g requiert deux arguments P et Q.")
            print_usage()
            sys.exit(84)

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

    if len(sys.argv) == 5:
        if sys.argv[3] != '-b':
            print(f"Erreur: Option '{sys.argv[3]}' non valide.")
            print_usage()
            sys.exit(84)

        use_block = True
        key = sys.argv[4]
    elif len(sys.argv) == 4:
        key = sys.argv[3]

    if key is None:
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
    print("USAGE")
    print("     ./my_pgp CRYPTO_SYSTEM MODE [OPTIONS] [key]")
    print("")
    print("  CRYPTO_SYSTEM")
    print("    \"xor\"        computation using XOR algorithm")
    print("    \"aes\"        computation using 128-bit AES algorithm")
    print("    \"rsa\"        computation using RSA algorithm")
    print("    \"pgp-xor\"    computation using both RSA and XOR algorithm")
    print("    \"pgp-aes\"    computation using both RSA and 128-bit AES algorithm")
    print("")
    print("  MODE")
    print("    -c           Cipher the MESSAGE")
    print("    -d           Decipher the MESSAGE")
    print("    -g P Q       for RSA only: Don't read a MESSAGE, but instead generate a public and private key pair from the prime number P and Q")
    print("")
    print("  OPTIONS")
    print("    -b           for XOR, AES and PGP, only works on one block. The MESSAGE and the symmetric key must be the same size")
    print("")
    print("  key        Key used to cipher/decipher MESSAGE (incompatible with -g MODE)")

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