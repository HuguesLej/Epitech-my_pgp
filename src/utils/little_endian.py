def hex_to_little_endian_bytes(hex_str):
    """Convert a hex string to bytes in little-endian order."""
    bytes_array = bytes.fromhex(hex_str)
    return bytes_array[::-1]

def bytes_to_little_endian_hex(byte_array):
    """Convert a byte array to a little-endian hex string."""
    return byte_array[::-1].hex()

def little_endian_hex_to_standard(hex_str):
    """Convert a little-endian hex string to a standard hex string."""
    bytes_array = bytes.fromhex(hex_str)
    standard_bytes = bytes_array[::-1]
    return standard_bytes.hex()

def little_endian_bytes_to_standard(byte_array):
    """Convert a little-endian byte array to a standard byte array."""
    return byte_array[::-1]
