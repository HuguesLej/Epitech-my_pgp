from math import gcd  # Importation de la fonction PGCD (Greatest Common Divisor)
from random import randrange  # Pour générer des nombres aléatoires (non utilisé ici)
import utils.little_endian as little_endian  # Module pour la conversion en little-endian

# Fonction pour calculer l'inverse modulaire de 'e' modulo 'phi'
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

FERMAT_PRIMES = [65537, 257, 17, 5, 3]

# Fonction pour générer une paire de clés RSA (publique et privée) à partir de deux nombres premiers 'p' et 'q'
def generate_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = None
    for fermat_prime in FERMAT_PRIMES:
        if 1 < fermat_prime < phi and gcd(fermat_prime, phi) == 1:
            e = fermat_prime
            break
    
    if e is None:
        raise ValueError("No valid Fermat prime found for e")
    
    d = mod_inverse(e, phi)

    public_key = little_endian.to_little_endian_hex(e) + '-' + little_endian.to_little_endian_hex(n)
    private_key = little_endian.to_little_endian_hex(d) + '-' + little_endian.to_little_endian_hex(n)

    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")
    
    return public_key, private_key

# Fonction principale pour la gestion des opérations RSA : génération, chiffrement, et déchiffrement
def rsa_encrypt_decrypt(message, args):

    if args['MODE'] == '-g':

        p = int(args['OPTIONS']['P'], 16)
        q = int(args['OPTIONS']['Q'], 16)
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
