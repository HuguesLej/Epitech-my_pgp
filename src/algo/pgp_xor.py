import utils.little_endian as little_endian

def xor_encrypt_decrypt(message, key_hex, mode):
    print(f"key hex: {key_hex}")
    try:
        key_bytes = bytes.fromhex(key_hex)
    except ValueError:
        raise ValueError(f"Key '{key_hex}' is not a valid hexadecimal number.")
    
    result_bytes = bytearray()
    
    if mode == '-c':
        message_bytes = message.encode()
    else:
        try:
            message_bytes = bytes.fromhex(message)
        except ValueError:
            raise ValueError(f"Message '{message}' is not a valid hexadecimal number.")

    for i in range(len(message_bytes)):
        result_bytes.append(message_bytes[i] ^ key_bytes[i % len(key_bytes)])
    
    if mode == '-c':
        return result_bytes.hex()
    else:
        return result_bytes.decode('utf-8', errors='replace') 

def rsa_encrypt_decrypt(message, key, mode):
    if mode == '-c':
        public_key = tuple(int.from_bytes(bytes.fromhex(x)[::-1], byteorder='big') for x in key.split('-'))
        e, n = public_key

        message_bytes = message.encode()[::-1]
        m = int.from_bytes(message_bytes, byteorder='big')

        c = pow(m, e, n)

        return little_endian.to_little_endian_hex(c)

    elif mode == '-d':
        private_key = tuple(int.from_bytes(bytes.fromhex(x)[::-1], byteorder='big') for x in key.split('-'))
        d, n = private_key

        cipher_bytes = bytes.fromhex(message)[::-1]
        c = int.from_bytes(cipher_bytes, byteorder='big')

        m = pow(c, d, n)

        decrypted_message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
        return decrypted_message[::-1].decode('utf-8', errors='replace')

def pgp_rsa_xor(message, args):
    symmetric_key, rsa_key = args['OPTIONS']['key'].split(':') 
    
    if args['MODE'] == '-c':

        ciphered_symmetric_key = rsa_encrypt_decrypt(symmetric_key, rsa_key, '-c')
        
        ciphered_message = xor_encrypt_decrypt(message, symmetric_key, '-c')

        print(ciphered_symmetric_key)
        return ciphered_message

    elif args['MODE'] == '-d':
        rsa_encrypted_symmetric_key = args['OPTIONS']['key'].split(':')[0]

        rsa_private_key = args['OPTIONS']['key'].split(':')[1]

        decrypted_symmetric_key = rsa_encrypt_decrypt(rsa_encrypted_symmetric_key, rsa_private_key, '-d')

        decrypted_message = xor_encrypt_decrypt(message, decrypted_symmetric_key, '-d')

        return decrypted_message