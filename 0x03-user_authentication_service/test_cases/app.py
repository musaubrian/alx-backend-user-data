#!/usr/bin/env python3
"""Simple flas app"""
from flask import Flask, jsonify, redirect, request, abort, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def status():
    """Return a response message"""
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """Register a new user"""
    email = request.form.get("email")
    pwd = request.form.get("password")

    try:
        new_user = AUTH.register_user(email=email, password=pwd)
        if new_user is not None:
            msg = {"email": new_user.email, "message": "user created"}
            return jsonify(msg)

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login user"""
    email = request.form.get("email")
    pwd = request.form.get("password")

    if not AUTH.valid_login(email, pwd):
        abort(401)
    session_id = AUTH.create_session(email=email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout a user"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session(session_id)
    if not user:
        abort(403)
        AUTH.destroy_session(user.id)
        return redirect(url_for("status"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Get the users profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session(session_id)
    if not user:
        abort(403)
    return ({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> tuple:
    """Reset password"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> tuple:
    """Update"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
