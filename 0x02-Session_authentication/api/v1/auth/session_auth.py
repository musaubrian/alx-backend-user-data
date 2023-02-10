#!/usr/bin/env python3
"""
module defines a SessionAuth class that inherits from class Auth
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """new authentication mechanism"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Returns a new sessionID for a user"""
        if not user_id or type(user_id) != str:
            return None

        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
