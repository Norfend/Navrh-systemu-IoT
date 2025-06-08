from repository.user_repository import login, register, logout


def login_service():
    return login()

def register_service():
    return register()

def logout_service():
    return logout()