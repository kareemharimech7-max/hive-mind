# 🐝 HIVE-MIND

*A Python 3 AsyncIO BitTorrent client built from scratch.*

Hive-Mind is an educational implementation of the **BitTorrent protocol**. The goal is to build a high-performance backend that communicates via WebSockets to a reactive frontend, visualizing the "swarm" of peers using SVG animations.

---

## 📡 Current status — Day 2: The Scout 📡

We can now parse torrents, generate a unique Peer ID, and contact HTTP Trackers to retrieve a list of active peers (IP:Port).

---

##  Features

### ✔️ Implemented
- **Custom B-encoding decoder** — Hand-written parser for the BitTorrent data format.
- **Torrent file parsing** — Extracts announce URLs, file names, and sizes.
- **Info-hash calculation** — Generates the SHA1 hash required to identify files in the swarm.
- **Peer ID generation** — Creates a unique 20-byte ID following Azureus-style conventions.
- **HTTP tracker client** — Communicates with trackers to announce presence and retrieve peer lists (compact mode supported).

### 🔜 Coming soon
- AsyncIO networking
- SVG swarm visualization

---

##  Installation & usage

### Prerequisites

- Python 3.8 or higher.
- An internet connection (to contact trackers).

### Setup

Clone the repository. Navigate to the project root:

```bash
cd HiveMind
```

### Running the client

Provide a valid .torrent file that uses an HTTP/HTTPS tracker (UDP support coming later).

```bash
python main.py /path/to/your/file.torrent
```

Expected output:

```text
🐝 HIVE-MIND CLIENT v0.1 Starting...
📦 TORRENT: debian-11.5.0-amd64-netinst.iso
   Size: 400 MB
   Hash: 12345abcde...

🆔 Generated Peer ID: -HM0001-928471029384

📡 Contacting Tracker...
✅ Found 50 peers in the swarm.

🟢 SUCCESS: Tracker returned 50 peers.
   Swarm Health: 1200 Seeders, 45 Leechers
   Sample Peers:
   ➡ 192.168.1.5:6881
   ➡ 89.23.14.2:51413
   ...
```

**Project structure**

```text
HiveMind/
├── hive_core/           # Backend logic
│   ├── bencoding.py     # Decodes integers, lists, dicts from raw bytes
│   ├── torrent.py       # Manages metadata and SHA1 hashing
│   ├── tracker.py       # (NEW) HTTP Tracker communication logic
│   └── utils.py         # (NEW) ID generation and IP decoding utilities
├── main.py              # Entry point
└── README.md            # You are here
```

## 📅 The 7-Day Development Roadmap

We are currently on Day 2.

1. **Day 1: The Foundation** (Parsing .torrent files & B-Encoding)
2. **Day 2: The Scout** (HTTP Tracker communication to find peers)
3. **Day 3: The Handshake** (AsyncIO TCP connection & Peer Handshake)
4. **Day 4: The Worker** (Piece Requesting & State Management)
5. **Day 5: The Architect** (Disk I/O & File Assembly)
6. **Day 6: The Nervous System** (WebSocket API Server)
7. **Day 7: The Face** (HTML5/JS Frontend with SVG Animations)

## ⚠️ Note on Trackers

Currently, this client only supports HTTP/HTTPS trackers. If you use a .torrent file that relies exclusively on UDP trackers (common with Magnet links or The Pirate Bay), the client will not be able to find peers yet. Look for torrents from official distributions (Ubuntu, Debian, Raspberry Pi) for testing.

## 📜 License

MIT License. Educational purposes only. Please respect copyright laws when downloading content.

🐝 Welcome to the swarm


