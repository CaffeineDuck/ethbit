import urllib.parse
from ethbit import web_client
import time
import hashlib
import hmac
import base64
import typing as t

__all__ = ("call_kraken",)


def get_kraken_signature(urlpath: str, data: dict[str, t.Any], api_sec: str) -> str:
    url_encoded_post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + url_encoded_post_data).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    signature = hmac.new(base64.b64decode(api_sec), message, hashlib.sha512)
    return base64.b64encode(signature.digest()).decode()


async def call_kraken(
    urlpath: str,
    data: dict[str, t.Any],
    api_key: str,
    api_sec: str,
) -> dict[str, t.Any]:
    baseurl = "https://api.kraken.com"
    data["nonce"] = str(int(time.time() * 1000))
    headers = {
        "API-Key": api_key,
        "API-Sign": get_kraken_signature(urlpath, data, api_sec),
    }
    data = (await web_client.post(baseurl + urlpath, headers=headers, data=data)).json()
    return data
