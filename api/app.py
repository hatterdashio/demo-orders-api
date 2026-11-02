"""A small order service: the sample app behind Hatterdash's demo."""
import os

from flask import Flask, abort, jsonify, request

from api import orders


def create_app(db_path=None):
    app = Flask(__name__)
    db = orders.connect(db_path or os.environ.get("ORDERS_DB", ":memory:"))

    @app.post("/orders")
    def create():
        customer = request.get_json()["customer"]
        return jsonify(id=orders.create_order(db, customer)), 201

    @app.get("/orders/<int:order_id>")
    def show(order_id):
        order = orders.get_order(db, order_id)
        if order is None:
            abort(404)
        return jsonify(order)

    return app
