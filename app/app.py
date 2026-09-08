"""
Mini Lutron-style device service.

This tiny Flask API stands in for one of Lutron's cloud services --
something a real DevOps platform would build, test, scan, package,
and deploy for hundreds of engineers.
"""
import time

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# In-memory "database" of smart lighting devices, purely for demo purposes.
DEVICES = {
    "1": {"id": "1", "name": "Living Room Dimmer", "brightness": 80, "on": True},
    "2": {"id": "2", "name": "Kitchen Shade", "brightness": 0, "on": False},
}

# --- Prometheus metrics ---
REQUEST_COUNT = Counter(
    "device_service_requests_total", "Total requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "device_service_request_latency_seconds", "Request latency", ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method, endpoint=request.path, status=response.status_code
    ).inc()
    return response


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


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