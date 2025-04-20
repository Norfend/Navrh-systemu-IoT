class User:
    def __init__(self):
        self.users = [
            {"login": "uporoego", "password": "123456"}
        ]

    def add_user(self, login, password):
        self.users.append({"login": login, "password": password})

    def get_user_password(self, login):
        for user in self.users:
            if user["login"] == login:
                return user["password"]
        return None