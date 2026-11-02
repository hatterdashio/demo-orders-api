"""A small order service: the sample app behind Hatterdash's demo."""
import os

from flask import Flask, abort, jsonify, request

from api import notify, orders


def create_app(db_path=None):
    app = Flask(__name__)
    db = orders.connect(db_path or os.environ.get("ORDERS_DB", ":memory:"))

    @app.post("/orders")
    def create():
        customer = request.get_json()["customer"]
        return jsonify(id=orders.create_order(db, customer)), 201

    @app.get("/orders/search")
    def search():
        return jsonify(orders.search_orders(db, request.args.get("customer", "")))

    @app.get("/orders/<int:order_id>")
    def show(order_id):
        order = orders.get_order(db, order_id)
        if order is None:
            abort(404)
        return jsonify(order)

    @app.post("/orders/<int:order_id>/ship")
    def ship(order_id):
        if orders.get_order(db, order_id) is None:
            abort(404)
        orders.mark_shipped(db, order_id)
        status = notify.notify_shipped(order_id, request.get_json()["tracking"])
        return jsonify(status=status)

    return app
