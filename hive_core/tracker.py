import urllib.request
import urllib.parse
import logging
from .bencoding import BDecoder
from .utils import decode_ip_port

# Configure Logging
log = logging.getLogger("Tracker")
logging.basicConfig(level=logging.INFO)

class TrackerManager:
    def __init__(self, torrent, peer_id):
        self.torrent = torrent
        self.peer_id = peer_id
        self.interval = 1800 # Default announce interval (30 mins)
        self.seeders = 0
        self.leechers = 0

    def connect(self):
        """
        Iterates through all available trackers until one works.
        """
        if not self.torrent.trackers:
            log.error("No trackers defined in torrent file.")
            return []

        for tracker_url in self.torrent.trackers:
            # Skip UDP for now (Day 2 limitation)
            if not tracker_url.startswith("http"):
                continue 
            
            log.info(f"Trying Tracker: {tracker_url}")
            
            peers = self._request_from_tracker(tracker_url)
            if peers:
                return peers
                
        log.error("Exhausted all trackers. No peers found.")
        return []

    def _request_from_tracker(self, url):
        """Internal helper to make the actual request to one URL."""
        params = {
            'info_hash': self.torrent.info_hash_bytes,
            'peer_id': self.peer_id,
            'port': 6881,
            'uploaded': 0,
            'downloaded': 0,
            'left': self.torrent.total_length,
            'compact': 1, # Request compact binary format
            'event': 'started'
        }
        
        # urlencode ensures the info_hash binary is percent-encoded correctly
        url_params = urllib.parse.urlencode(params)
        full_url = f"{url}?{url_params}"

        try:
            # We use 'Transmission/2.94' as User-Agent to look like a standard client.
            # Some trackers block default python agents.
            req = urllib.request.Request(full_url, headers={'User-Agent': 'Transmission/2.94'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    log.warning(f"Tracker {url} returned status {response.status}")
                    return None
                
                response_data = response.read()
                
            # Decode Response (Bencoded)
            tracker_resp = BDecoder(response_data).decode()
            
            if not tracker_resp:
                return None

            # Check for failure
            if 'failure reason' in tracker_resp:
                reason = tracker_resp['failure reason']
                if isinstance(reason, bytes): reason = reason.decode()
                log.warning(f"Tracker {url} Error: {reason}")
                return None

            # Update stats
            self.interval = tracker_resp.get('interval', 1800)
            self.seeders = tracker_resp.get('complete', 0)
            self.leechers = tracker_resp.get('incomplete', 0)

            # Parse Peers
            peers_blob = tracker_resp['peers']
            return self._parse_peers(peers_blob)

        except Exception as e:
            # We catch generic exceptions here so the loop can continue to the next tracker
            log.warning(f"Failed to connect to {url}: {e}")
            return None

    def _parse_peers(self, peers_data):
        """
        Parses the 'peers' field. 
        """
        peers_list = []

        # Case A: Binary String (Compact Model) - Most common
        if isinstance(peers_data, bytes):
            log.info(f"Received {len(peers_data)} bytes of compact peer data.")
            for i in range(0, len(peers_data), 6):
                chunk = peers_data[i : i+6]
                if len(chunk) < 6:
                    break
                try:
                    ip, port = decode_ip_port(chunk)
                    peers_list.append((ip, port))
                except Exception:
                    continue

        # Case B: List of Dictionaries (Old Model)
        elif isinstance(peers_data, list):
            log.info("Received dictionary model peer data.")
            for p in peers_data:
                if 'ip' in p and 'port' in p:
                    ip = p['ip'].decode() if isinstance(p['ip'], bytes) else p['ip']
                    port = p['port']
                    peers_list.append((ip, port))

        log.info(f"✅ Found {len(peers_list)} peers.")
        return peers_list