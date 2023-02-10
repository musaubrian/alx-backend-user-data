#!/usr/bin/env python3
"""handles all routes for the Session authentication"""


from os import getenv
from flask import jsonify, request
from models.user import User


@app_views.route(
        "/auth_session/login", methods=["POST"], strict_slashes=False)
def login_session():
    """ """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")

    if not user_email:
        return jsonify(error="email missing"), 400
    if not user_pwd:
        return jsonify(error="password missing"), 400

    try:
        users = User.search({"email": user_email})
    except Exception:
        return jsonify(error="no user found for this email"), 404
    if not users:
        return jsonify(error="no user found for this email"), 404
    for user in users:
        if user.is_valid_password(user_pwd):
            user_id = user.id
            from api.v1.app import auth

            session_id = auth.create_session(user_id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv("SESSION_NAME"), session_id)
            return response
        else:
            return jsonify(error="wrong password"), 401
    return jsonify(error="no user found for this email"), 404


@app_views.route(
        "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    DELETE /auth_session/logout
    Return:
      - Response
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
