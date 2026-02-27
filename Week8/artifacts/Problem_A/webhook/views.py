"""
Webhook route handler.
POST /webhook receives JSON and builds a log message.
Bug: when 'source' is omitted or null, source is None and concatenation raises TypeError.
"""
from flask import Blueprint, request, jsonify

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json() or {}
    # These can be None if key is missing or value is null
    source = data.get("source")
    event = data.get("event", "")
    payload = data.get("payload", "")

    # BUG: When source is None (e.g. POST body {"event": "ping"}), this line raises:
    # TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
    log_message = source + ": " + event + " - " + str(payload)

    return jsonify({"received": True, "log": log_message}), 200
