import hashlib
from .bencoding import BDecoder, bencode

class Torrent:
    def __init__(self, filepath):
        with open(filepath, 'rb') as f:
            raw = f.read()
        
        meta = BDecoder(raw).decode()
        self.info = meta['info']
        
        # --- NEW TRACKER LOGIC ---
        self.trackers = []
        
        # 1. Get the main announce URL
        if 'announce' in meta:
            self.trackers.append(meta['announce'].decode('utf-8'))
        
        # 2. Get the backup list (announce-list)
        # It's usually a list of lists: [['url1'], ['url2', 'url3']]
        if 'announce-list' in meta:
            for tier in meta['announce-list']:
                for url_bytes in tier:
                    try:
                        url = url_bytes.decode('utf-8')
                        if url not in self.trackers:
                            self.trackers.append(url)
                    except:
                        pass # Ignore malformed URLs
        
        # Use the first one as default for display
        self.announce_url = self.trackers[0] if self.trackers else None
        
        # --- CALCULATE INFO HASH ---
        self.info_hash_bytes = hashlib.sha1(bencode(self.info)).digest()
        self.info_hash_hex = self.info_hash_bytes.hex()
        
        # --- PARSE FILE METADATA ---
        self.name = self.info['name'].decode()
        self.piece_length = self.info['piece length']
        
        if 'files' in self.info:
            # Multi-file torrent
            self.total_length = sum(f['length'] for f in self.info['files'])
            self.files = [(f['path'][0].decode(), f['length']) for f in self.info['files']]
        else:
            # Single-file torrent
            self.total_length = self.info['length']
            self.files = [(self.name, self.total_length)]
            
        hashes = self.info['pieces']
        self.piece_hashes = [hashes[i:i+20] for i in range(0, len(hashes), 20)]
        self.total_pieces = len(self.piece_hashes)

    def __str__(self):
        tracker_count = len(self.trackers)
        return (f"📦 TORRENT: {self.name}\n"
                f"   Size: {self.total_length / (1024*1024):.2f} MB\n"
                f"   Pieces: {self.total_pieces} x {self.piece_length / 1024:.0f} KB\n"
                f"   Trackers Found: {tracker_count}\n"
                f"   Hash: {self.info_hash_hex}")