from fastapi import Request
import hashlib
import json
from typing import Dict

class FingerprintService:
    @staticmethod
    def generate_fingerprint(request: Request) -> Dict:
        """Generate a browser fingerprint from request headers"""
        headers = dict(request.headers)
        fingerprint_data = {
            'user_agent': headers.get('user-agent', ''),
            'accept_language': headers.get('accept-language', ''),
            'accept_encoding': headers.get('accept-encoding', ''),
            'accept': headers.get('accept', ''),
            'connection': headers.get('connection', ''),
            'dnt': headers.get('dnt', ''),  # Do Not Track
            'sec_ch_ua': headers.get('sec-ch-ua', ''),  # Browser info
            'sec_ch_ua_platform': headers.get('sec-ch-ua-platform', '')  # OS info
        }
        
        # Generate hash of fingerprint
        fingerprint_hash = hashlib.sha256(
            json.dumps(fingerprint_data, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            'hash': fingerprint_hash,
            'data': fingerprint_data
        } 