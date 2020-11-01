from werkzeug.security import generate_password_hash, check_password_hash

from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domain.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    user = repo.get_user(username)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password) # 不知道这个 function在哪 import？
    # Create and store the new User, with password encrypted.
    user = User(username, password_hash)
    repo.add_user(user)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str, repo: AbstractRepository): # 应该是login的检查
    authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    user_dict = {
        'username': user.user_name,
        'password': user.password
    }
    return user_dict









