# hive_core/peer.py
import asyncio
import struct
import logging

log = logging.getLogger("Peer")

class PeerConnection:
    def __init__(self, ip, port, torrent, my_peer_id):
        self.ip = ip
        self.port = port
        self.torrent = torrent
        self.my_peer_id = my_peer_id
        
        self.reader = None
        self.writer = None
        self.connected = False
        self.peer_choking = True  # By default, peers choke us (refuse to give data)

    async def start(self):
        """
        Main entry point. Connects, Handshakes, then closes (for now).
        """
        try:
            # 1. Establish TCP Connection (5 second timeout)
            await asyncio.wait_for(self._connect(), timeout=5.0)
            
            # 2. Perform Handshake
            success = await self._handshake()
            if not success:
                await self.close()
                return

            log.info(f"✅ HANDSHAKE SUCCESS: {self.ip}:{self.port}")
            self.connected = True
            
            # --- DAY 3 STOP POINT ---
            # In a real client, we would start a "Listen Loop" here.
            # For today, we just want to prove we can connect.
            await self.close() 

        except asyncio.TimeoutError:
            pass # Peer is offline or firewalled
        except ConnectionRefusedError:
            pass # Peer rejected us
        except Exception as e:
            # log.debug(f"Error with {self.ip}: {e}")
            await self.close()

    async def _connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)

    async def _handshake(self):
        """
        Sends and verifies the BitTorrent Handshake.
        """
        # --- BUILD PACKET ---
        pstr = b"BitTorrent protocol"
        pstrlen = len(pstr) # 19
        reserved = b'\x00' * 8
        
        handshake_packet = (
            bytes([pstrlen]) + 
            pstr + 
            reserved + 
            self.torrent.info_hash_bytes + 
            self.my_peer_id
        )
        
        # --- SEND ---
        self.writer.write(handshake_packet)
        await self.writer.drain()
        
        # --- RECEIVE ---
        # We expect exactly 68 bytes back
        try:
            data = await self.reader.readexactly(68)
        except:
            return False
        
        # --- VERIFY ---
        # 1. Check Protocol Header
        if data[0:20] != bytes([19]) + b"BitTorrent protocol":
            return False

        # 2. Check Info Hash (Bytes 28 to 48)
        # This is CRITICAL. If this doesn't match, they have a different file.
        recv_info_hash = data[28:48]
        if recv_info_hash != self.torrent.info_hash_bytes:
            log.warning(f"{self.ip} - Wrong Info Hash.")
            return False

        return True

    async def close(self):
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except:
                pass
        self.connected = False