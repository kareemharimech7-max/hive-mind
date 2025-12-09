# hive_core/torrent.py
import hashlib
import math
from .bencoding import BDecoder, bencode

class Torrent:
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            raw = f.read()
        
        meta = BDecoder(raw).decode()
        self.announce_url = meta['announce'].decode()
        self.info = meta['info']
        
        # CRITICAL: Calculate SHA1 hash of the 'info' dict
        # This is what we send to the tracker and peers.
        self.info_hash_bytes = hashlib.sha1(bencode(self.info)).digest()
        self.info_hash_hex = self.info_hash_bytes.hex()
        
        self.name = self.info['name'].decode()
        self.piece_length = self.info['piece length']
        
        # Calculate total size
        if 'files' in self.info:
            self.total_length = sum(f['length'] for f in self.info['files'])
            self.files = [(f['path'][0].decode(), f['length']) for f in self.info['files']]
        else:
            self.total_length = self.info['length']
            self.files = [(self.name, self.total_length)]
            
        # Break apart the long binary string of piece hashes
        hashes = self.info['pieces']
        self.piece_hashes = [hashes[i:i+20] for i in range(0, len(hashes), 20)]
        self.total_pieces = len(self.piece_hashes)

    def __str__(self):
        return (f"📦 TORRENT: {self.name}\n"
                f"   Size: {self.total_length / (1024*1024):.2f} MB\n"
                f"   Pieces: {self.total_pieces} x {self.piece_length / 1024:.0f} KB\n"
                f"   Hash: {self.info_hash_hex}")