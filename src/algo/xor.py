#!/usr/bin/python3

import src.utils.little_endian as little_endian
import sys


def xor_encrypt_decrypt(message, args):

    if args['OPTIONS']['block_mode'] == False:
        sys.exit(84)

    key_hex = args['OPTIONS']['key']
    if (args['MODE'] == '-c'):
        key_bytes = little_endian.hex_to_little_endian_bytes(key_hex)
    else:
        key_bytes = bytes.fromhex(key_hex)
    result_bytes = bytearray()

    if args['OPTIONS']['block_mode']:
        message_bytes = message.encode() if args['MODE'] == '-c' else bytes.fromhex(message)
        block_size = len(key_bytes)
        for i in range(0, len(message_bytes), block_size):
            block = message_bytes[i:i + block_size]
            if len(block) < block_size:
                exit(84)
        for i in range(len(message_bytes)):
            result_bytes.append(message_bytes[i] ^ key_bytes[i % len(key_bytes)])
    if args['MODE'] == '-c':
        return little_endian.bytes_to_little_endian_hex(result_bytes)  
    else:
        return result_bytes.decode('utf-8', errors='replace')[::-1]

def xor_algo(input_data, key):
    result_bytes = bytearray()
    for i in range(len(input_data)):
        result_bytes.append(input_data[i] ^ key[i % len(key)])
    return bytes(result_bytes)