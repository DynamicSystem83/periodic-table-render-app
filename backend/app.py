import os

from flask import Flask, jsonify, request
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    allowed_origins = os.environ.get("CORS_ORIGINS", "*")
    CORS(app, origins=allowed_origins)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/api/periodic-table-encode-simple")
    def caesar():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")
        shift = payload.get("shift", 3)

        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400

        try:
            shift = int(shift)
        except (TypeError, ValueError):
            return jsonify({"error": "shift must be an integer"}), 400

        return jsonify({"output": encode_simple(text, shift), "shift": shift})

    return app


def encode_simple(text, shift):
    shifted = []
    normalized_shift = shift % 26

    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            shifted.append(chr((ord(char) - base + normalized_shift) % 26 + base))
        elif "A" <= char <= "Z":
            base = ord("A")
            shifted.append(chr((ord(char) - base + normalized_shift) % 26 + base))
        else:
            shifted.append(char)

    return "".join(shifted)


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
