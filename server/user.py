from enum import Enum
from socket import socket

from common.common_utils import generate_key

class UserState(Enum):
    ENTERING_NAME = 1
    ENTERING_PASSWORD = 2
    LOGGED_IN = 3

class User:
    def __init__(self, name: str, sock: socket):
        self.name = name
        self.sock = sock
        self.state = UserState.ENTERING_NAME
        self.password = ''
        self.key = None
    
    def change_state(self, state: UserState):
        self.state = state
    
    def change_password(self, password: str):
        self.password = password
        self.key = generate_key(password)

class JsonUser:
    def __init__(self, password: str, friends):
        self.password = password
        self.friends = friends