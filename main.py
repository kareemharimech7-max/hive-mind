# main.py
import sys
import asyncio
import logging
from hive_core.torrent import Torrent
from hive_core.tracker import TrackerManager
from hive_core.utils import generate_peer_id
from hive_core.peer import PeerConnection

# Configure nicer logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)

async def process_peer(semaphore, ip, port, torrent, my_id):
    """
    Limits concurrent connections using a semaphore.
    """
    async with semaphore:
        peer = PeerConnection(ip, port, torrent, my_id)
        await peer.start()

async def main():
    print("🐝 HIVE-MIND CLIENT v0.1 - DAY 3")
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.torrent>")
        return

    try:
        # 1. Load Torrent
        t_path = sys.argv[1]
        torrent = Torrent(t_path)
        print(f"📦 TORRENT: {torrent.name}")
        
        # 2. Identity
        my_id = generate_peer_id()
        
        # 3. Tracker
        print("📡 Contacting Tracker...")
        tracker = TrackerManager(torrent, my_id)
        peers_list = tracker.connect()

        if not peers_list:
            print("🔴 FAILURE: No peers found.")
            return

        print(f"🟢 SUCCESS: Found {len(peers_list)} potential peers.")
        print("⚡ STARTING SWARM HANDSHAKE (Max 50 concurrent)...")
        print("-----------------------------------")

        # 4. Async Connection Swarm
        sem = asyncio.Semaphore(50) # Allow 50 parallel connections
        tasks = []
        
        for ip, port in peers_list:
            task = asyncio.create_task(
                process_peer(sem, ip, port, torrent, my_id)
            )
            tasks.append(task)

        # Wait for everyone to finish
        await asyncio.gather(*tasks)
        
        print("-----------------------------------")
        print("✅ DAY 3 COMPLETE: Handshake logic verified.")

    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")