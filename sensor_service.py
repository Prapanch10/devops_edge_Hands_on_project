import time
import random
import threading
from flask import Flask, jsonify
from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CollectorRegistry
)

app = Flask(__name__)

# -------------------------
# Custom Prometheus Registry
# -------------------------
registry = CollectorRegistry()

# -------------------------
# Large static data (created once)
# -------------------------
data_blob = "X" * 5_000_000

# -------------------------
# Metrics (lightweight)
# -------------------------
REQUEST_COUNT = Counter(
    "sensor_requests_total",
    "Total sensor requests",
    registry=registry
)

CPU_SPIKE = Gauge(
    "sensor_cpu_spike",
    "Simulated CPU spike state",
    registry=registry
)

PROCESS_LATENCY = Gauge(
    "sensor_processing_latency_seconds",
    "Processing time",
    registry=registry
)

# -------------------------
# Shared state
# -------------------------
current_latency = 0.0
cpu_spike_state = 0

# -------------------------
# Background sensor work
# -------------------------
def sensor_loop():
    global current_latency, cpu_spike_state
    while True:
        start = time.time()

        # Simulated lightweight sensor work
        time.sleep(random.uniform(0.01, 0.05))

        current_latency = time.time() - start
        cpu_spike_state = random.randint(0, 1)

        PROCESS_LATENCY.set(current_latency)
        CPU_SPIKE.set(cpu_spike_state)

        # Run once per second
        time.sleep(1)

# Start background thread once
threading.Thread(target=sensor_loop, daemon=True).start()

# -------------------------
# Metrics endpoint (VERY LIGHT)
# -------------------------
@app.route("/metrics")
def metrics():
    REQUEST_COUNT.inc()
    return generate_latest(registry)

# -------------------------
# Sensor endpoint
# -------------------------
@app.route("/sensor")
def sensor():
    if random.random() < 0.2:
        return jsonify({"data": data_blob})
    return jsonify({"status": "ok"})

# -------------------------
# App start (no reloader)
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, use_reloader=False)
