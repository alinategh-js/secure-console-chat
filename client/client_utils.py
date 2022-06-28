from socket import socket
from cryptography.fernet import Fernet
from common.configs import BUFFERSIZE, HEADERSIZE, KEY

from client.client_configs import read_key

def send_message(cs: socket, msg: str):
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    key = read_key()
    if key == None:
        key = KEY
    fernet = Fernet(key)
    msg = fernet.encrypt(bytes(msg, 'utf-8'))
    cs.send(msg)

def receive_new_message(cs: socket):
    full_msg = b''
    key = read_key()
    if key == None:
        key = KEY
    fernet = Fernet(key)
    while True:
        full_msg += cs.recv(BUFFERSIZE)
        try:
            decrypted_msg = fernet.decrypt(full_msg)
            msglen = int(decrypted_msg[:HEADERSIZE].strip())
            full_msg = decrypted_msg.decode('utf-8')
            return full_msg[HEADERSIZE:]
        except:
            pass