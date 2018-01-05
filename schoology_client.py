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

    async def post_update(self, group_id, text, attachments=None):
        payload = {'body': text}
        if attachments:
            payload['attachments'] = [a.to_json() for a in attachments]
        return await self.post(f"{API_BASE_URL}/groups/{group_id}/updates", payload)

    async def post(self, destination, payload, headers=None):
        _head = self.get_auth_header()
        if headers is not None:
            _head.update(headers)
        async with aiohttp.ClientSession() as session:
            async with session.post(destination, data=json.dumps(payload), headers=_head) as resp:
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


class Attachment:
    def __init__(self, _type='url', title='Unnamed', url='', thumbnail=''):
        self.type = _type
        self.title = title
        self.url = url
        self.thumbnail = thumbnail

    @classmethod
    def from_discord_attachment(cls, attachment):
        return cls('url', attachment['filename'], attachment['url'], attachment['url'])

    def to_json(self):
        return {
            'type': self.type,
            'title': self.title,
            'url': self.url,
            'thumbnail': self.thumbnail
        }


class HTTPError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message
