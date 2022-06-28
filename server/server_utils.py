from datetime import datetime
import json
from typing import Dict
from cryptography.fernet import Fernet

from common.common_utils import generate_key
from server.user import JsonUser, User, UserState
from common.configs import BUFFERSIZE, HEADERSIZE, KEY
from server.online_users_manager import get_online_user_by_name

def send_message(user: User, msg: str):
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    if user.key != None:
        key = user.key
    else:
        key = KEY
    fernet = Fernet(key)
    msg = fernet.encrypt(bytes(msg, 'utf-8'))
    user.sock.send(msg)

def receive_new_message(user: User):
    full_msg = b''
    if user.key != None:
        key = user.key
    else:
        key = KEY
    fernet = Fernet(key)
    while True:
        full_msg += user.sock.recv(BUFFERSIZE)
        try:
            decrypted_msg = fernet.decrypt(full_msg)
            msglen = int(decrypted_msg[:HEADERSIZE].strip())
            full_msg = decrypted_msg.decode('utf-8')
            return full_msg[HEADERSIZE:]
        except:
            pass

def send_instructions(user: User, greet: bool = False):
    msg = """\nUseful commands:

    /help  ->  To see this menu.
    /pm [friend_name] [message_text]  ->  To send a message to a friend.
    /friends  ->  To see a list of your friends.
    /add-friend [user_name] ->  To add a person to your friends list."""

    if greet:
        msg = "You have successfuly logged in!\n" + msg
    send_message(user, msg)

def extract_command(user: User, msg: str):
    msg = msg.strip()
    if msg.startswith("/help"):
        send_instructions(user)
        
    elif msg.startswith("/pm"):
        try:
            command_parts = msg.split(' ')
            friend_name = command_parts[1]
            message_text = " ".join(command_parts[2:])
        except:
            send_message(user, "Wrong usage of command!\n/pm [friend_name] [message_text]")
            return
        send_pm(user, friend_name, message_text)
    
    elif msg.startswith("/add-friend"):
        try:
            command_parts = msg.split(' ')
            user_name = command_parts[1]
        except:
            send_message(user, "Wrong usage of command!\n/add-friend [user_name]")
            return
        add_friend(user, user_name)

    elif msg.startswith("/friends"):
        send_friends_list(user)
    
    else:
        send_message(user, "Invalid command!")

def send_pm(user: User, friend_name: str, msg: str):
    # check if friend_name is in user's friends list
    with open('server/users.json', 'r+') as f:
        data = json.load(f)
        friends_list = json.loads(data[user.name])['friends']
        if friend_name in friends_list:
            # check if target user is online
            friend = get_online_user_by_name(friend_name)
            if friend == None:
                send_message(user, "Your friend is not online right now.")
                return
            else:
                if friend.state == UserState.LOGGED_IN:
                    send_message(friend, f"[{datetime.now()}] [{user.name}]: {msg}")
                else:
                    send_message(user, "Your friend is not online right now.")
                return
        else:
            send_message(user, "You cannot send a message to someone who is not your friend.\nUse /add-friend to add them to your friends list.")

def add_friend(user: User, user_name: str):
    with open('server/users.json', 'r+') as f:
        data = json.load(f)
        try:
            found_target_user = data[user_name]
        except:
            send_message(user, "User does not exist!")
            return

        friends_list = json.loads(data[user.name])['friends']
        if user_name in friends_list:
            send_message(user, "User is already in your friends list.")
            return
        else:
            friends_list.append(user_name)
            send_message(user, f"{user_name} has been added to your friends list.")
            jsonStr = make_json_string(data[user.name], {"friends": friends_list})
            data[user.name] = jsonStr # <--- add `id` value
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part

def make_json_string(user_json_data, data_to_update_dict: Dict[str, any] = None):
    try:
        loaded_data = json.loads(user_json_data)
        password = loaded_data['password']
        friends_list = loaded_data['friends']
        if data_to_update_dict != None:
            new_password = data_to_update_dict.get('password')
            new_friends_list = data_to_update_dict.get('friends')
            if new_password != None:
                password = new_password
            if new_friends_list != None:
                friends_list = new_friends_list
        
        jsonStr = json.dumps(JsonUser(password, friends_list).__dict__)
        return jsonStr
    except:
        return

def send_friends_list(user: User):
    with open('server/users.json', 'r+') as f:
        try:
            data = json.load(f)
            friends_list = json.loads(data[user.name])['friends']
            result = "Your friends: " + ", ".join(friends_list)
            send_message(user, result)
        except:
            pass