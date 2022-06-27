import socket
from threading import Thread

from client.client_configs import change_password
from client.client_utils import receive_new_message, send_message

KEY = b'1MqViQOaXP4Qc1sh2cQXGBYH9dFBeCNWdbVM2cVKc0g='
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5003

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

last_msg_sent = ""

def listen_for_messages():
    while True:
        msg = receive_new_message(client_socket)
        if msg.find("You have successfuly logged in!") != -1:
            change_password(last_msg_sent)
        print(msg)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    to_send =  input()

    if to_send.lower() == '/quit':
        break

    send_message(client_socket, to_send)
    last_msg_sent = to_send

# close the socket
client_socket.close()