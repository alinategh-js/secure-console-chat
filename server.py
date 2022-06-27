import socket
import json
from threading import Thread
from server.online_users_manager import get_online_user, pop_online_user, set_online_user
from server.user import JsonUser, User, UserState

from server.server_utils import extract_command, receive_new_message, send_instructions, send_message

SERVER_IP = '127.0.0.1'
PORT = 5003

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(5)

print(f"Server is now listening on {SERVER_IP}:{PORT}")

def listen_for_client(cs: socket, address):
    user = get_online_user(address)
    if user == None:
        print(f"New connection from {address}")
        user = User("", cs)
        set_online_user(address, user)
        send_message(user, "Welcome to the server.\nPlease enter your nickname: ")

    while True:
        try:
            # keep listening for a message from `cs` socket
            user = get_online_user(address)
            msg = receive_new_message(user)
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            pop_online_user(address)
            break
        else:
            if user != None:
                if user.state == UserState.ENTERING_NAME:
                    user.name = msg
                    user.change_state(UserState.ENTERING_PASSWORD)
                    send_message(user, "Please enter your password: ")

                elif user.state == UserState.ENTERING_PASSWORD:
                    with open('server/users.json', 'r+') as f:
                        data = json.load(f)
                        try:
                            found_user = data[user.name]
                        except Exception as e:
                            found_user = None

                        if found_user == None:
                            # create new user
                            jsonStr = json.dumps(JsonUser(msg, []).__dict__)
                            data[user.name] = jsonStr # <--- add `id` value
                            f.seek(0)        # <--- should reset file position to the beginning.
                            json.dump(data, f, indent=4)
                            f.truncate()     # remove remaining part
                            user.change_state(UserState.LOGGED_IN)
                            send_instructions(user, True)
                        else:
                            # check if password is correct
                            if json.loads(found_user)['password'] == msg:
                                user.change_state(UserState.LOGGED_IN)
                                send_instructions(user, True)
                                user.change_password(msg)
                            else:
                                send_message(user, "Wrong password!\nEither try again or choose another nickname.")
                elif user.state == UserState.LOGGED_IN:
                    extract_command(user, msg)
            else:
                break

while True:
    (client_socket, address) = server_socket.accept()
    
    # we also need one thread for processing new client messages
    t2 = Thread(target=listen_for_client, args=(client_socket, address))
    t2.daemon = True
    t2.start()