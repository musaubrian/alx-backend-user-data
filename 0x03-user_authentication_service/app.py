#!/usr/bin/env python3
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def status():
    """ """
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


if __name__ == "__main__":
    port_num = 5000
    app.run(host="0.0.0.0", port=port_num)
