import json
import requests
import blaulichtsms.constants as constants
from typing import Union


class LoginRequest:
    def __init__(self, customer_id: str, username: str, password: str) -> None:
        self.customerId = customer_id
        self.username = username
        self.password = password


def login(login: LoginRequest) -> Union[str, None]:
    response = requests.post(constants.LOGIN,
                             data=json.dumps(login.__dict__),
                             headers={'Content-Type': 'application/json'})
    if response.ok:
        return response.json()['token']
    else:
        return None
