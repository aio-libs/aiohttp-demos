import bcrypt


def generate_password_hash(password):
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password_hash(plain_password, password_hash):
    plain_password_bin = plain_password.encode('utf-8')
    password_hash_bin = password_hash.encode('utf-8')
    is_correct = bcrypt.checkpw(plain_password_bin, password_hash_bin)
    return is_correct
