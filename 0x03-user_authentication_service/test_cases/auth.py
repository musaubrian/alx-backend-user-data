#!/usr/bin/env python3
"""Module deals with authentication"""
from db import DB, InvalidRequestError, User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import checkpw, gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """Returns bytes as a salted hash of the input password"""
    hashed_pwd = hashpw(password.encode("utf-8"), gensalt())

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create a new User"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password).decode("utf-8")
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if user credentials are okay"""
        if email is None and password is None:
            return False

        try:
            user_records = self._db.find_user_by(email=email)
            hashed_pwd = user_records.hashed_password
            result = checkpw(password.encode("utf-8"), hashed_pwd.encode())
            return result
        except (NoResultFound, InvalidRequestError):
            return False

