# main.py
import sys
import asyncio
from hive_core.torrent import Torrent

async def main():
    print("🐝 HIVE-MIND CLIENT v0.1 Starting...")
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.torrent>")
        return

    try:
        t_path = sys.argv[1]
        torrent = Torrent(t_path)
        print(torrent)
        print("\n✅ DAY 1 COMPLETE: Torrent parsed successfully.")
        print("NEXT STEP: Connecting to Tracker at", torrent.announce_url)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    # We use asyncio.run to prepare for future async networking
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass