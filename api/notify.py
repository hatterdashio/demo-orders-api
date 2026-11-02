"""Tells the carrier when an order ships."""
import hashlib
import hmac
import json
import os
import time

import certifi
import requests

CARRIER_URL = os.environ.get("CARRIER_URL", "http://hooks.acme-freight.io/orders")


def signature(body):
    secret = os.environ["CARRIER_SECRET"].encode()
    return hmac.new(secret, body, hashlib.sha256).hexdigest()


def post_to_carrier(body):
    return requests.post(
        CARRIER_URL,
        data=body,
        headers={"Content-Type": "application/json", "X-Signature": signature(body)},
        timeout=5,
        verify=certifi.where(),
    )


def notify_shipped(order_id, tracking_number):
    body = json.dumps({"order": order_id, "tracking": tracking_number}).encode()
    response = post_to_carrier(body)
    if response.status_code == 409:
        # The carrier already has this shipment.
        return "duplicate"
    if response.status_code >= 500:
        time.sleep(1)
        response = post_to_carrier(body)
    response.raise_for_status()
    return "sent"
