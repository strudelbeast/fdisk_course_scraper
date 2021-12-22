import json
import requests
from blaulichtsms import constants
from blaulichtsms import authcache
from typing import Optional
from datetime import datetime, timedelta


class LoginRequest:
    def __init__(self, customer_id: str, username: str, password: str) -> None:
        self.customerId = customer_id
        self.username = username
        self.password = password


def login(login_dto: LoginRequest) -> Optional[authcache.TokenCache]:
    cached_token = authcache.get_token(login_dto.customerId, login_dto.username)
    if cached_token is not None:
        return cached_token

    response = requests.post(constants.LOGIN,
                             data=json.dumps(login_dto.__dict__),
                             headers={'Content-Type': 'application/json'})
    if response.ok:
        expire_time = datetime.now() + timedelta(hours=24)
        return authcache.cache_token(login_dto.customerId, login_dto.username, response.json()['token'], expire_time)
    else:
        return None
