#!/usr/bin/env python3
from flask import Flask, jsonify, request
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
    """ """
    email = request.form.get("email")
    pwd = request.form.get("password")

    try:
        new_user = AUTH.register_user(email=email, password=pwd)
        if new_user is not None:
            msg = {"email": new_user.email, "message": "user created"}
            return jsonify(msg)

    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    port_num = 5000
    app.run(host="0.0.0.0", port=port_num)
