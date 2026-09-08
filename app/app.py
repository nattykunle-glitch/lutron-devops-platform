"""
Mini Lutron-style device service.

This tiny Flask API stands in for one of Lutron's cloud services --
something a real DevOps platform would build, test, scan, package,
and deploy for hundreds of engineers.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" of smart lighting devices, purely for demo purposes.
DEVICES = {
    "1": {"id": "1", "name": "Living Room Dimmer", "brightness": 80, "on": True},
    "2": {"id": "2", "name": "Kitchen Shade", "brightness": 0, "on": False},
}


@app.get("/health")
def health():
    """Used by the pipeline's smoke test and by uptime checks."""
    return jsonify(status="ok"), 200


@app.get("/devices")
def list_devices():
    return jsonify(list(DEVICES.values())), 200


@app.get("/devices/<device_id>")
def get_device(device_id):
    device = DEVICES.get(device_id)
    if not device:
        return jsonify(error="device not found"), 404
    return jsonify(device), 200


@app.patch("/devices/<device_id>/brightness")
def set_brightness(device_id):
    device = DEVICES.get(device_id)
    if not device:
        return jsonify(error="device not found"), 404

    payload = request.get_json(silent=True) or {}
    brightness = payload.get("brightness")

    if not isinstance(brightness, int) or not (0 <= brightness <= 100):
        return jsonify(error="brightness must be an integer 0-100"), 400

    device["brightness"] = brightness
    device["on"] = brightness > 0
    return jsonify(device), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)