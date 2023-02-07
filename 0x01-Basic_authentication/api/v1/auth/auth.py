#!/usr/bin/env python3
"""
Defines a class to manage authentication
"""

from typing import List
from flask import request


class Auth:
    """
    defines a class Auth that manages api authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns:
            True if the path is not in the list of strings excluded_paths
            True if path is None
            True if excluded_paths is None or empty
            False if path is in excluded_paths
            must be slash tolerant:
                path=/api/v1/status and path=/api/v1/status/ must be returned
                False if excluded_paths contains /api/v1/status/
        """
        if path is None or not excluded_paths:
            return True
        for p in excluded_paths:
            if p.endswith("*") and path.startswith(p[:1]):
                return False
            elif p in {path, path + "/"}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None"""
        return None
