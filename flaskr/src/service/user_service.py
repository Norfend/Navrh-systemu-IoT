import logging

from flask import request

from repository.user_repository import login, register, logout

module_logger = logging.getLogger(__name__)

def login_service():
    if request.method == "POST":
        module_logger.debug("Request received to perform login")
    elif request.method == "GET":
        module_logger.debug("Request received to download login page")
    return login()

def register_service():
    if request.method == "POST":
        module_logger.debug("Request received to perform registration")
    elif request.method == "GET":
        module_logger.debug("Request received to download registration page")
    return register()

def logout_service():
    module_logger.debug("Request received to perform logout")
    return logout()