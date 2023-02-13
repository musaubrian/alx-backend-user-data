#!/usr/bin/env python3
"""Module deals with authentication"""
from db import DB
from bcrypt import gensalt, hashpw


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Returns bytes as a salted hash of the input password"""
        hashed_pwd = hashpw(password.encode("utf-8"), gensalt())

        return hashed_pwd
