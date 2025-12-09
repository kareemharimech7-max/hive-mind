import sys
import asyncio
import logging
from hive_core.torrent import Torrent
from hive_core.tracker import TrackerManager
from hive_core.utils import generate_peer_id

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

async def main():
    print("🐝 HIVE-MIND CLIENT v0.1 Starting...")
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.torrent>")
        return

    try:
        # Step 1: Load Torrent
        t_path = sys.argv[1]
        torrent = Torrent(t_path)
        print(torrent)
        
        # Step 2: Generate Identity
        my_id = generate_peer_id()
        print(f"\n🆔 Generated Peer ID: {my_id.decode()}")

        # Step 3: Contact Tracker
        # This now uses the logic that tries multiple trackers if one fails
        print("\n📡 Contacting Tracker...")
        tracker = TrackerManager(torrent, my_id)
        peers = tracker.connect()

        # Step 4: Display Results
        if peers:
            print(f"\n🟢 SUCCESS: Tracker returned {len(peers)} peers.")
            print(f"   Swarm Health: {tracker.seeders} Seeders, {tracker.leechers} Leechers")
            print("\n   Sample Peers:")
            for ip, port in peers[:10]: # Show first 10
                print(f"   ➡ {ip}:{port}")
                
            print(f"\n   ...and {len(peers)-10} others.")
            print("\n✅ DAY 2 COMPLETE: Tracker communication fixed.")
        else:
            print("\n🔴 FAILURE: Could not retrieve peers from any tracker in the list.")

    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    try:
        # Windows AsyncIO fix (good habit to keep even for Day 2)
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(main())
    except KeyboardInterrupt:
        pass