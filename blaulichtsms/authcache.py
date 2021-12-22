from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Optional
import os
import json
from blaulichtsms import constants


class TokenCache:
    def __init__(self, customer_id: str, username: str, token: str, expires: datetime) -> None:
        self.customerId = customer_id
        self.username = username
        self.token = token
        self.expires = expires
        if not self.is_valid():
            raise Exception("Json not parseable")

    def is_valid(self) -> bool:
        return self.customerId is not None and \
               self.username is not None and \
               self.token is not None and \
               self.expires is not None


def cache_token(customer_id: str, username: str, token: str, expires: datetime) -> Optional[TokenCache]:
    try:
        with open(constants.TOKENS_FILE, "w") as file:
            token_cache = TokenCache(
                    customer_id,
                    username,
                    token,
                    expires)
            json.dump(
                token_cache.__dict__,
                file,
                default=default_converter)
            return token_cache
    except Exception:
        print("Exception while caching token")


def get_token(customer_id: str, username: str) -> Optional[TokenCache]:
    if not os.path.isfile(constants.TOKENS_FILE):
        return None

    token = get_cached_token()

    if token is None:
        return None

    if token.customerId == customer_id and \
            token.username == username and \
            token.expires > (datetime.now() + timedelta(seconds=5)):
        return token


def get_cached_token() -> Optional[TokenCache]:
    with open(constants.TOKENS_FILE, 'r') as f:
        try:
            cached_token_dict = json.load(f)
            return TokenCache(cached_token_dict['customerId'],
                              cached_token_dict['username'],
                              cached_token_dict['token'],
                              datetime.fromisoformat(cached_token_dict['expires']))
        except (JSONDecodeError, Exception):
            print("Could not parse cached tokens")
    return None


def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
