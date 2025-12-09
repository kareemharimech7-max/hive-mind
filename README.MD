#  HIVE-MIND

*A Python 3 AsyncIO BitTorrent client built from scratch.*

Hive-Mind is an educational implementation of the **BitTorrent protocol**, built to demystify how torrents work internally. The long-term goal is to create a **high-performance AsyncIO backend** that communicates with a **WebSocket-powered frontend**, visualizing the swarm using animated SVG graphics.

---

##  Current status  Day 1: Foundation

We can currently read, decode, and interpret `.torrent` files.

---

##  Features

###  Implemented
- **Custom B-encoding decoder**  Hand-written parser for BitTorrent integers, strings, lists, and dictionaries.
- **Torrent file parsing**  Extracts announce URLs, file metadata, and piece information.
- **Info-hash calculation**  Computes the SHA-1 hash that uniquely identifies a torrent.

###  Coming soon
- Tracker communication (HTTP & UDP)
- AsyncIO peer networking
- Piece request / block exchange logic
- Disk I/O & file assembly
- WebSocket API server
- SVG-based swarm visualization

---

##  Installation & usage

### Prerequisites

- Python 3.8+

### Setup

Clone the repository or create the folder structure manually.

### Running the client

To test the torrent parser, run:

```bash
python main.py /path/to/your/file.torrent
```

Expected output (example):

```text
 HIVE-MIND CLIENT v0.1 Starting...
 TORRENT: ubuntu-22.04.1-live-server-amd64.iso
   Size: 1.38 GB
   Pieces: 2824 x 512 KB
   Hash: 12345abcde...

 DAY 1 COMPLETE: Torrent parsed successfully.
NEXT STEP: Connecting to tracker...
```

**Project structure**

```text
HiveMind/
 hive_core/           # Backend logic
    bencoding.py     # Decodes integers, lists, dicts from raw bytes
    torrent.py       # Manages metadata and SHA1 hashing
 main.py              # Entry point
 README.md            
```

##  7-day development roadmap

1. Day 1  Foundation: Parsing .torrent files & B-encoding
2. Day 2  Scout: HTTP/UDP tracker communication
3. Day 3  Handshake: AsyncIO peer TCP connections
4. Day 4  Worker: Piece requesting & state management
5. Day 5  Architect: Disk I/O & file assembly
6. Day 6  Nervous system: WebSocket API server
7. Day 7  Face: HTML5/JS frontend with SVG animations

##  License

MIT License  Educational purposes only. Please respect copyright laws when downloading content.

 Welcome to the swarm
