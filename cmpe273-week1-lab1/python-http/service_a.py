from flask import Flask, request, jsonify, g
import time
import logging

SERVICE_NAME = "service-a"

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


@app.route("/echo", methods=["GET"])
def echo():
    msg = request.args.get("msg", "")
    return jsonify({"echo": msg}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
