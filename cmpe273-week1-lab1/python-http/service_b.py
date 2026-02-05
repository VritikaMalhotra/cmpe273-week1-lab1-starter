from flask import Flask, request, jsonify, g
import requests
import time
import logging

SERVICE_NAME = "service-b"
SERVICE_A_URL = "http://127.0.0.1:8080/echo"
TIMEOUT_SECONDS = 2

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    latency_ms = (time.time() - g.start_time) * 1000
    logger.info({
        "service": SERVICE_NAME,
        "endpoint": request.path,
        "status": response.status_code,
        "latency_ms": round(latency_ms, 2)
    })
    response.headers["Content-Type"] = "application/json"
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/call-echo", methods=["GET"])
def call_echo():
    msg = request.args.get("msg", "")

    try:
        response = requests.get(
            SERVICE_A_URL,
            params={"msg": msg},
            timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()

        return jsonify({
            "service_b": "ok",
            "service_a_response": response.json()
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Service A: {e}")
        return jsonify({
            "error": "Service A unavailable"
        }), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
