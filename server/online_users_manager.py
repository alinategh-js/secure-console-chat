from server.user import User

online_users_dict = dict()

def get_online_user(address):
    return online_users_dict.get(address)

def pop_online_user(address):
    return online_users_dict.pop(address)

def set_online_user(address, user: User):
    try:
        online_users_dict[address] = user
    except:
        pass

def get_online_user_by_name(name: str):
    try:
        users = list(online_users_dict.values())
        user = [x for x in users if x.name == name][0]
        return user
    except:
        return None