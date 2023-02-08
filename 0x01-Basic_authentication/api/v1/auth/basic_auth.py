#!/usr/bin/env python3
"""
Module defines a class BasicAuth that inherits from Auth
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Inherits class Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Return None if authorization_header is None
        Return None if authorization_header is not a string
        Return None if authorization_header doesn’t start by Basic
            (with a space at the end)
        Otherwise, return the value after Basic (after the space)
        """
        if (
            not authorization_header
            or type(authorization_header) != str
            or not authorization_header.startswith("Basic")
        ):
            return
        return "".join(authorization_header.split(" ")[1:])
