#  HIVE-MIND

*A Python 3 AsyncIO BitTorrent client built from scratch.*

Hive-Mind is an educational implementation of the **BitTorrent protocol**. The goal is to build a high-performance backend that communicates via WebSockets to a reactive frontend, visualizing the "swarm" of peers using SVG animations.

---

##  Current status  Day 3: The Handshake 

We have moved from passive observation to active participation. The client now spawns an asynchronous swarm of TCP connections, performs the BitTorrent Handshake, and verifies peer identities.

---

##  Features

###  Implemented
- **Custom B-encoding decoder**  Hand-written parser for the BitTorrent data format.
- **Smart tracker client**  Supports HTTP/HTTPS multi-tracker failover (handles announce-list and 503 errors).
- **AsyncIO networking**  Uses non-blocking sockets with asyncio.gather and Semaphores to handle high concurrency.
- **The handshake**  Implements the binary handshake protocol (`<pstrlen><pstr><reserved><info_hash><peer_id>`) to authenticate peers.

###  Coming soon
- Message protocol (Choke/Unchoke/Interested)
- Piece manager
- SVG swarm visualization

---

##  Installation & usage

### Prerequisites

- Python 3.8 or higher.
- An internet connection.

### Setup

Clone the repository. Navigate to the project root:

```bash
cd HiveMind
```

### Running the client

Provide a valid .torrent file.

```bash
python main.py /path/to/your/file.torrent
```

Expected output (Day 3):

```text
 HIVE-MIND CLIENT v0.1 - DAY 3
 TORRENT: ubuntu-22.04.1-live-server-amd64.iso

 Contacting Tracker...
 SUCCESS: Found 50 potential peers.
 STARTING SWARM HANDSHAKE (Max 50 concurrent)...
-----------------------------------
[INFO]  HANDSHAKE SUCCESS: 185.12.9.1:51413
[INFO]  HANDSHAKE SUCCESS: 201.55.12.8:6881
[INFO]  HANDSHAKE SUCCESS: 45.12.88.99:40000
...
-----------------------------------
 DAY 3 COMPLETE: Handshake logic verified.
```

**Project structure**

```text
HiveMind/
 hive_core/           # Backend logic
    bencoding.py     # Decodes integers, lists, dicts from raw bytes
    torrent.py       # Manages metadata and SHA1 hashing
    tracker.py       # HTTP Multi-Tracker communication logic
    peer.py          # (NEW) Async TCP Peer Connection & Handshake
    utils.py         # ID generation and IP decoding utilities
 main.py              # Entry point
 README.md            # You are here
```

##  The 7-Day Development Roadmap

We are currently on Day 3.

1. **Day 1: The Foundation** (Parsing .torrent files & B-Encoding)
2. **Day 2: The Scout** (Tracker Communication & Peer Discovery)
3. **Day 3: The Handshake** (AsyncIO TCP Swarm & Protocol Handshake)
4. **Day 4: The Worker** (Message Loop, Choking/Unchoking states)
5. **Day 5: The Architect** (Piece Requesting & Data Collection)
6. **Day 6: The Nervous System** (WebSocket API Server)
7. **Day 7: The Face** (HTML5/JS Frontend with SVG Animations)

##  Technical Notes regarding Day 3

**Concurrency:** We use `asyncio.Semaphore(50)` to limit the client to 50 simultaneous connection attempts. This prevents OS-level "Too many open files" errors.

**Timeouts:** Connections have a hard 5-second timeout. If a peer doesn't handshake fast enough, we drop them to keep the swarm moving.

##  License

MIT License. Educational purposes only. Please respect copyright laws when downloading content.

 Welcome to the swarm
