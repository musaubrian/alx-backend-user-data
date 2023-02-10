#!/usr/bin/env python3
"""
API authentication module
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if API routes require authentication"""
        if path is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith("*") and path.startswith(i[:-1]):
                return False
            elif i in {path, path + "/"}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks if Authorization request header is present
        & contains values"""
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Return None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None

        _my_session_id = os.getenv("SESSION_NAME")
        res = request.cookies.get(_my_session_id)
        return res
