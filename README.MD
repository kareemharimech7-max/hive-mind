# 🐝 HIVE-MIND
*A Python 3 AsyncIO BitTorrent Client built from scratch.*

Hive-Mind is an educational implementation of the **BitTorrent protocol**, built to demystify how torrents work internally.  
The long-term goal is to create a **high-performance AsyncIO backend** that communicates with a **WebSocket-powered frontend**, visualizing the entire swarm using animated SVG graphics.

---

## 🚧 Current Status: DAY 1 — FOUNDATION PHASE
We can currently **read, decode, and interpret `.torrent` files**.

---

## 📋 Features

### ✔️ Implemented
- **Custom B-Encoding Decoder**  
  Hand-written parser for BitTorrent integers, strings, lists, and dictionaries.
- **Torrent File Parsing**  
  Extracts announce URLs, file metadata, and piece information.
- **Info Hash Calculation**  
  Generates the SHA-1 hash needed to uniquely identify a torrent in the swarm.

### 🔜 Coming Soon
- Tracker Communication (HTTP & UDP)
- AsyncIO Peer Networking
- Piece Request / Block Exchange Logic
- Disk I/O & File Assembly
- WebSocket API Server
- SVG-Based Swarm Visualization

---

## 🛠️ Installation & Usage

### Prerequisites
- Python **3.8+**

### Setup
Clone the repository or create the folder structure manually:

```bash
cd HiveMind
Running the Client
To test the torrent parser, pass in a valid .torrent file:

bash
Copy code
python main.py /path/to/your/file.torrent
Expected Output
yaml
Copy code
🐝 HIVE-MIND CLIENT v0.1 Starting...
📦 TORRENT: ubuntu-22.04.1-live-server-amd64.iso
   Size: 1.38 GB
   Pieces: 2824 x 512 KB
   Hash: 12345abcde...

✅ DAY 1 COMPLETE: Torrent parsed successfully.
NEXT STEP: Connecting to Tracker...
📂 Project Structure
graphql
Copy code
HiveMind/
├── hive_core/           # Backend Logic
│   ├── bencoding.py     # Decodes integers, lists, dicts from raw bytes
│   └── torrent.py       # Manages metadata and SHA1 hashing
├── main.py              # Entry point
└── README.md            # You are here
📅 The 7-Day Development Roadmap
Day 1 — The Foundation: Parsing .torrent files & B-Encoding

Day 2 — The Scout: HTTP/UDP tracker communication

Day 3 — The Handshake: AsyncIO peer TCP connections

Day 4 — The Worker: Piece requesting & state management

Day 5 — The Architect: Disk I/O & file assembly

Day 6 — The Nervous System: WebSocket API server

Day 7 — The Face: HTML5/JS frontend with SVG animations

📜 License
MIT License
Educational purposes only. Please respect copyright laws when downloading content.

🐝 Welcome to the swarm