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
