#!/usr/bin/python3

import src.utils.little_endian as little_endian


sbox = [
#   0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, # 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, # 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, # 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, # 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, # 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, # 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, # 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, # 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, # 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, # 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, # a
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, # b
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, # c
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, # d
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, # e
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16  # f
]


def ListToColBasedMatrix(lst: list[int]) -> list[list[int]]:
    return [[lst[col + row * 4] for row in range(4)] for col in range(4)]


def ColBasedMatrixToList(matrix: list[list[int]]) -> list[int]:
    return [matrix[row][col] for col in range(4) for row in range(4)]


def ListWordsToLittleEndian(lst: list[int]) -> list[int]:
    result = []

    for i in range(0, 16, 4):
        word = lst[i:i + 4]
        result.extend(word[::-1])
    
    return result


def PrintMatrix(matrix: list[list[int]]) -> None:
    print()
    print("| Column 0 | Column 1 | Column 2 | Column 3 |")
    print("|----------|----------|----------|----------|")
    for row in range(4):
        print(f"| 0x{matrix[row][0]:02x}     | 0x{matrix[row][1]:02x}     | 0x{matrix[row][2]:02x}     | 0x{matrix[row][3]:02x}     |")
    print()


def GaloisMult(a: int, b: int) -> int:
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11b
        b >>= 1
    return res


def AddRoundKey(state: list[list[int]], subKey: list[list[int]]) -> list[list[int]]:
    for row in range(4):
        for col in range(4):
            state[row][col] ^= subKey[row][col]
    return state


def RotWordLeft(word: list[int]) -> list[int]:
    return [word[1], word[2], word[3], word[0]]


def RotWordRight(word: list[int]) -> list[int]:
    return [word[3], word[0], word[1], word[2]]


def SubWord(word: list[int]) -> list[int]:
    return [sbox[byte] for byte in word]


def RevSubWord(word: list[int]) -> list[int]:
    return [sbox.index(byte) for byte in word]


def ShiftRows(state: list[list[int]]) -> list[list[int]]:
    for row in range(1, 4):
        for _ in range(row):
            state[row] = RotWordLeft(state[row])
    return state


def RevShiftRows(state: list[list[int]]) -> list[list[int]]:
    for row in range(1, 4):
        for _ in range(row):
            state[row] = RotWordRight(state[row])
    return state


def SubBytes(state: list[list[int]]) -> list[list[int]]:
    for i in range(0, 4):
        state[i] = SubWord(state[i])
    return state


def RevSubBytes(state: list[list[int]]) -> list[list[int]]:
    for i in range(0, 4):
        state[i] = RevSubWord(state[i])
    return state


def MixColumns(state: list[list[int]]) -> list[list[int]]:
    for col in range(4):
        s0 = state[0][col]
        s1 = state[1][col]
        s2 = state[2][col]
        s3 = state[3][col]

        state[0][col] = GaloisMult(0x02, s0) ^ GaloisMult(0x03, s1) ^ s2 ^ s3
        state[1][col] = s0 ^ GaloisMult(0x02, s1) ^ GaloisMult(0x03, s2) ^ s3
        state[2][col] = s0 ^ s1 ^ GaloisMult(0x02, s2) ^ GaloisMult(0x03, s3)
        state[3][col] = GaloisMult(0x03, s0) ^ s1 ^ s2 ^ GaloisMult(0x02, s3)
    return state


def RevMixColumns(state: list[list[int]]) -> list[list[int]]:
    for col in range(4):
        s0 = state[0][col]
        s1 = state[1][col]
        s2 = state[2][col]
        s3 = state[3][col]

        state[0][col] = GaloisMult(0x0e, s0) ^ GaloisMult(0x0b, s1) ^ GaloisMult(0x0d, s2) ^ GaloisMult(0x09, s3)
        state[1][col] = GaloisMult(0x09, s0) ^ GaloisMult(0x0e, s1) ^ GaloisMult(0x0b, s2) ^ GaloisMult(0x0d, s3)
        state[2][col] = GaloisMult(0x0d, s0) ^ GaloisMult(0x09, s1) ^ GaloisMult(0x0e, s2) ^ GaloisMult(0x0b, s3)
        state[3][col] = GaloisMult(0x0b, s0) ^ GaloisMult(0x0d, s1) ^ GaloisMult(0x09, s2) ^ GaloisMult(0x0e, s3)
    return state


def RCon(word: list[int], i: int) -> list[int]:
    if i == 0:
        word[0] = 0
    word[0] = 1
    for _ in range(i - 1):
        if word[0] & 0x80:
            word[0] = (word[0] << 1) ^ 0x11b
        else:
            word[0] = word[0] << 1
    return word


def ExpandKeys(cypher_key: list[int]) -> list[list[int]]:
    words = [cypher_key[i * 4:(i + 1) * 4] for i in range(4)]

    for i in range(4, 44):
        temp = words[i - 1]
        if i % 4 == 0:
            temp = SubWord(RotWordLeft(temp))
            temp[0] ^= RCon([0x00] * 4, i // 4)[0]
        words.append([words[i - 4][j] ^ temp[j] for j in range(4)])

    keys: list[list[int]] = []
    for i in range(0, len(words), 4):
        key: list[int] = []
        for j in range(4):
            key.extend(words[i + j])
        keys.append(key)
    return keys


def Encrypt(lst: list[int], keys: list[list[int]]) -> list[int]:
    state = ListToColBasedMatrix(lst)

    state = AddRoundKey(state, ListToColBasedMatrix(keys[0]))

    for i in range(9):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, ListToColBasedMatrix(keys[i + 1]))

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, ListToColBasedMatrix(keys[10]))

    return ColBasedMatrixToList(state)


def Decrypt(lst: list[int], keys: list[list[int]]) -> list[int]:
    state = ListToColBasedMatrix(lst)

    state = AddRoundKey(state, ListToColBasedMatrix(keys[10]))

    for i in range(9, 0, -1):
        state = RevShiftRows(state)
        state = RevSubBytes(state)
        state = AddRoundKey(state, ListToColBasedMatrix(keys[i]))
        state = RevMixColumns(state)

    state = RevShiftRows(state)
    state = RevSubBytes(state)
    state = AddRoundKey(state, ListToColBasedMatrix(keys[0]))

    return ColBasedMatrixToList(state)


def aes_encrypt_decrypt(message, args):
    ## WORKS ONLY WITH BLOCK MODE ENABLED
    ## WORKS ONLY WITH '-c' MODE

    # print("message: ", message)
    # print("args: ", args)

    hex_key = [int(args["OPTIONS"]["key"][i:i + 2], 16) for i in range(0, len(args["OPTIONS"]["key"]), 2)]
    hex_lst = [ord(char) for char in message]

    cypher_key = ListWordsToLittleEndian(hex_key)
    state_lst = hex_lst
    keys = ExpandKeys(cypher_key)

    # for i in range(len(keys)):
    #     print(f"key {i}: {[hex(byte) for byte in keys[i]]}")

    encrypted_lst = Encrypt(state_lst, keys)
    # PrintMatrix(ListToColBasedMatrix(encrypted_lst))
    # print(f"encrypted_lst: {[hex(byte) for byte in encrypted_lst]}")
    result = ListWordsToLittleEndian(encrypted_lst)
    # PrintMatrix(ListToColBasedMatrix(result))
    # print(f"encrypted_lst: {[hex(byte) for byte in result]}")
    encrypted_message = "".join([format(byte, "02x") for byte in result])
    # print("encrypted_message: ", encrypted_message)


    return encrypted_message
