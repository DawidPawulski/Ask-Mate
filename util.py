import data_manager
import bcrypt
from flask import redirect, make_response

def toggle_order(order):
    if order == 'ASC':
        return 'DESC'
    elif order == 'DESC':
        return 'ASC'

def upload_picture(picture, target):
    if picture("image")[0]:
        file = picture("image")[0]
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
        return filename
    else:
        filename = 'default_avatar.jpg'
        return filename

def check_new_user_username_login(login):
    info_existing_users = data_manager.get_exist_users_info()
    for info in info_existing_users:
        if info['login'] == login:
            return False
    return True


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)

