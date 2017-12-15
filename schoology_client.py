import json
import logging
import time

import aiohttp as aiohttp
import oauth2 as oauth

log = logging.getLogger(__name__)

API_BASE_URL = "https://api.schoology.com/v1"


class SchoologyClient:
    def __init__(self, credentials_file):
        with open(credentials_file) as f:
            _data = json.load(f)
            self.consumer_key = _data['consumer_key']
            self.consumer_secret = _data['consumer_secret']
        self.session = aiohttp.ClientSession()

    async def post_update(self, group_id, text):
        payload = {'body': text}
        return await self.post(f"{API_BASE_URL}/groups/{group_id}/updates", payload)

    async def post(self, destination, payload, headers=None):
        _head = self.get_auth_header()
        if headers is not None:
            _head.update(headers)
        async with self.session.post(destination, json=payload, headers=_head) as resp:
            if 399 < resp.status < 600:  # 4xx, 5xx errors
                raise HTTPError(resp.status, await resp.text())
            js = await resp.json()
            log.debug(str(js))
            return js

    def get_auth_header(self):
        headers = {
            'Host': "api.schoology.com",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'Authorization': f"OAuth realm=\"Schoology%20API\","
                             f"oauth_consumer_key=\"{self.consumer_key}\","
                             f"oauth_token=\"\","
                             f"oauth_nonce=\"{oauth.generate_nonce()}\","
                             f"oauth_timestamp=\"{int(time.time())}\","
                             f"oauth_signature_method=\"PLAINTEXT\","
                             f"oauth_version=\"1.0\","
                             f"oauth_signature=\"{self.consumer_secret}%26\""
        }
        return headers


class HTTPError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message
