#!/usr/bin/env python3
"""
Module implements a hash_password function that returns a hashed password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    returns a hashed password
    ---
    Args::
        password(str): string to be hashed
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Returns True if provided password matches the hashed password
    else Returns False
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True

    return False
