#!/usr/bin/env python3
"""Module deals with authentication"""
from typing import Union
from db import DB, InvalidRequestError, User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from bcrypt import checkpw, gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """Returns bytes as a salted hash of the input password"""
    hashed_pwd = hashpw(password.encode("utf-8"), gensalt())

    return hashed_pwd


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    new_uuid = uuid.uuid4()

    return str(new_uuid)


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

    def create_session(self, email: str) -> Union[str, None]:
        """
        generates a new UUID, stores it in the db as the user’s session_id,
        then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except (ValueError, NoResultFound):
            return None

    def get_user_from_session(self, session_id: str) -> Union[str, None]:
        """
        Returns corresponding user or None based on the sessionID
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates sessionID ot None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            if user.reset_token:
                return user.reset_token
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode("utf-8")
            self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None
            )
        except NoResultFound:
            raise
