#!/usr/bin/env python3
"""Simple flas app"""
from flask import Flask, jsonify, request, abort
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
    resp.set_cookie("session_id": session_id)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
