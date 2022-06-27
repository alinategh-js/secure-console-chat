from common.common_utils import generate_key

password = ""
key = None

def change_password(new_password: str):
    global password
    global key
    password = new_password
    key = generate_key(password)

def read_password():
    return password

def read_key():
    return key