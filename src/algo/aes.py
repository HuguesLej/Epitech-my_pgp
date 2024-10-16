#!/usr/bin/python3

import src.utils.little_endian as little_endian

def aes_encrypt(message: str, key):
    result_bytes = bytearray()
    state_matrix = [[0 for i in range(4)] for j in range(4)]
    key_matrix = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            state_matrix[j][i] = ord(message[i * 4 + j])
            key_matrix[j][i] = key[i * 4 + j]

def aes_decrypt(message, key):
    result_bytes = bytearray()

def aes_encrypt_decrypt(message, args):
    if args.OPTIONS.block_mode == False:
        print("Error: AES not implemented yet without block mode.")
        return None

    key_hex = args.OPTIONS.key
    if args.MODE == '-c':
        result_bytes = aes_encrypt(message, little_endian.hex_to_little_endian_bytes(key_hex))
    else:
        result_bytes = aes_decrypt(message, bytes.fromhex(key_hex))

    if args.MODE == '-c':
        return little_endian.bytes_to_little_endian_hex(result_bytes)
    else:
        return result_bytes.decode('utf-8', errors='replace')[::-1]
