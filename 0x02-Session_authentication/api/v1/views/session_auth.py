#!/usr/bin/env python3
"""handles all routes for the Session authentication"""


from os import getenv
from flask import jsonify, request
from models.user import User


@app_views.route(
        "/auth_session/login", methods=["POST"], strict_slashes=False)
def login_session():
    """implement the login functionality"""
    email = request.form.get("email")
    pwd = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not pwd:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(pwd):
            user_id = user.id
            from api.v1.app import auth

            session_id = auth.create_session(user_id)
            res = jsonify(user.to_json())
            res.set_cookie(getenv("SESSION_NAME"), session_id)
            return res
        else:
            return jsonify({"error": "wrong password"}), 401
    return jsonify({"error": "no user found for this email"}), 404
