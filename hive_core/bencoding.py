# hive_core/bencoding.py
import logging

class BDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.index = 0

    def decode(self):
        if self.index >= len(self.data):
            return None
        char = self.data[self.index:self.index+1]
        
        if char == b'i':
            return self._decode_int()
        elif char == b'l':
            return self._decode_list()
        elif char == b'd':
            return self._decode_dict()
        elif char in b'0123456789':
            return self._decode_string()
        else:
            raise ValueError(f"Unknown bencoding char at {self.index}: {char}")

    def _decode_int(self):
        self.index += 1 # Skip 'i'
        end = self.data.find(b'e', self.index)
        if end == -1: raise ValueError("Invalid Int")
        num = int(self.data[self.index:end])
        self.index = end + 1
        return num

    def _decode_string(self):
        colon = self.data.find(b':', self.index)
        length = int(self.data[self.index:colon])
        self.index = colon + 1
        val = self.data[self.index : self.index+length]
        self.index += length
        return val

    def _decode_list(self):
        self.index += 1 # Skip 'l'
        res = []
        while self.data[self.index:self.index+1] != b'e':
            res.append(self.decode())
        self.index += 1
        return res

    def _decode_dict(self):
        self.index += 1 # Skip 'd'
        res = {}
        while self.data[self.index:self.index+1] != b'e':
            key = self.decode()
            if isinstance(key, bytes):
                key = key.decode('utf-8', 'ignore')
            val = self.decode()
            res[key] = val
        self.index += 1
        return res

def bencode(data):
    # We need a simple encoder to calculate hashes later
    if isinstance(data, int): return f"i{data}e".encode()
    if isinstance(data, bytes): return f"{len(data)}:".encode() + data
    if isinstance(data, str): return f"{len(data)}:".encode() + data.encode()
    if isinstance(data, list): return b"l" + b"".join(bencode(x) for x in data) + b"e"
    if isinstance(data, dict):
        return b"d" + b"".join(bencode(k) + bencode(v) for k, v in sorted(data.items())) + b"e"