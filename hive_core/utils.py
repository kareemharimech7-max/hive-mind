# hive_core/utils.py
import random
import string
import socket
import struct

def generate_peer_id():
    """
    Generates a 20-byte Peer ID.
    Format: -<Client><Version>-<Random>
    Example: -HM0001-123456789012
    """
    client_id = "-HM0001-"
    random_nums = ''.join(random.choices(string.digits, k=12))
    return (client_id + random_nums).encode('utf-8')

def decode_ip_port(bytes_data):
    """
    Decodes a 6-byte sequence into an IP:Port tuple.
    Bytes 0-3: IP Address
    Bytes 4-5: Port (Big Endian)
    """
    if len(bytes_data) != 6:
        raise ValueError("Invalid peer data length")
    
    # unpack "!IH": ! = Network (Big Endian), I = Int (4 bytes), H = Short (2 bytes)
    ip_int, port = struct.unpack("!IH", bytes_data)
    ip_str = socket.inet_ntoa(struct.pack("!I", ip_int))
    return ip_str, port