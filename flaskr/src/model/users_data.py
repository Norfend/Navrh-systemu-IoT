from werkzeug.security import generate_password_hash

class User:
    def __init__(self):
        self.users = {
            "uporoego": generate_password_hash("123456", method="pbkdf2:sha256", salt_length=16)
        }

    def add_user(self, login, password):
        if login in self.users:
            return False
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        self.users[login] = hashed_password
        return True

    def get_user_password(self, login):
        return self.users.get(login)