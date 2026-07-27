import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from mendeleev import element
import numpy as np

# Create a default random number generator
rng = np.random.default_rng()


def create_app():
    app = Flask(__name__)
    allowed_origins = os.environ.get("CORS_ORIGINS", "*")
    CORS(app, origins=allowed_origins)


    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})


    @app.post("/api/periodic-table-encode-simple")
    def encode_simple():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")

        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400

        shift_amount = rng.integers(low=1, high=10)
        shift_symbol = element(int(shift_amount)).symbol
        shift_symbol = shift_symbol.upper()

        encoded_text = ""
        encoded_text += shift_symbol

        text = text.lower()
        for character in text:
            if character.isalpha():
                number = ord(character) - ord("a") + 1 # a = 0 + 1, z = 25 + 1
                number = number + shift_amount + rng.integers(low=0, high=4)*27
                encoded_text += atomic_number_to_symbol(number)
            elif character == " ":
                number = 26 + 1 # space = 26 + 1
                number = number + shift_amount + rng.integers(low=0, high=4)*27
                encoded_text += atomic_number_to_symbol(number)
            else:
                encoded_text += character

        return jsonify({"output": encoded_text})


    @app.post("/api/periodic-table-decode-simple")
    def decode_simple():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")

        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400

        first_sentence = text.split(".")[0]
        if len(first_sentence)%2 == 0:
            shift_symbol = "".join(first_sentence[0:2])
            text = text[2:]
        else:
            shift_symbol = "".join(first_sentence[0:1])
            text = text[1:]
        shift_symbol = shift_symbol.title()
        shift_amount = element(shift_symbol).atomic_number

        decoded_text = ""
        i = 0
        while i < len(text):
            if text[i] == ".":
                decoded_text += text[i]
                i += 1
            else:
                symbol = "".join(text[i:i+2])
                i += 2
                number = symbol_to_atomic_number(symbol)
                number = number - shift_amount - 1
                number = number%27
                app.logger.error("Informational message in terminal %d" % number)
                if number == 36:
                    decoded_text += " "
                else:
                    decoded_text += chr(number + ord("a"))

        return jsonify({"output": decoded_text})


    @app.post("/api/periodic-table-encode-complex")
    def encode_complex():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")

        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400

        shift_amount = rng.integers(low=1, high=10)
        shift_symbol = element(int(shift_amount)).symbol
        shift_symbol = shift_symbol.upper()

        encoded_text = ""
        encoded_text += shift_symbol

        text = text.lower()
        for character in text:
            if character.isalpha():
                number = ord(character) - ord("a") + 1 # a = 0 + 1, z = 25 + 1
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            elif character.isnumeric():
                number = ord(character) - ord("0") + 26 + 1 # 0 = 0 + 26 + 1, 9 = 26 + 9 + 1
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            elif character == " ":
                number = 26 + 10 + 1 # space = 26 + 10 + 1
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            elif character == ".":
                number = 26 + 10 + 1 + 1 # space = 26 + 10 + 1 + 1
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            elif character == ",":
                number = 26 + 10 + 1 + 2 # space = 26 + 10 + 1 + 2
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            elif character == "!":
                number = 26 + 10 + 1 + 3 # space = 26 + 10 + 1 + 3
                number = number + shift_amount + rng.integers(low=0, high=2)*40
                encoded_text += atomic_number_to_symbol(number)
            else:
                encoded_text += character
        return jsonify({"output": encoded_text})


    @app.post("/api/periodic-table-decode-complex")
    def decode_complex():
        payload = request.get_json(silent=True) or {}
        text = payload.get("text", "")

        if not isinstance(text, str):
            return jsonify({"error": "text must be a string"}), 400

        first_sentence = text.split(".")[0]
        if len(first_sentence)%2 == 0:
            shift_symbol = "".join(first_sentence[0:2])
            text = text[2:]
        else:
            shift_symbol = "".join(first_sentence[0:1])
            text = text[1:]
        shift_symbol = shift_symbol.title()
        shift_amount = element(shift_symbol).atomic_number

        decoded_text = ""
        i = 0
        while i < len(text):
            symbol = "".join(text[i:i+2])
            i += 2
            print(symbol)
            number = symbol_to_atomic_number(symbol)
            number = number - shift_amount - 1
            number = number%40
            if number == 36:
                decoded_text += " "
            elif number == 37:
                decoded_text += "."
            elif number == 38:
                decoded_text += ","
            elif number == 39:
                decoded_text += "!"
            elif (number >= 25) and (number <= 35):
                decoded_text += chr(number - 26  + ord("0"))
            else:
                decoded_text += chr(number + ord("a"))

        return jsonify({"output": decoded_text})


    return app


def atomic_number_to_symbol(number):
    """
    Convert an atomic number to an element symbol. Doubles single character symbols.
    """
    number = int(number)
    symbol = ""
    if (number > 0) and (number < 119):
        symbol = element(number).symbol
    else:
        raise Exception("number out of range")
    
    if len(symbol) == 1:
        symbol = symbol + symbol
    return symbol.upper()


def symbol_to_atomic_number(symbol):
    """
    Convert an element symbol to an atomic number. Reduces double symbols into a single symbol.
    """
    if symbol[0] == symbol[1]:
        symbol = symbol[0]
    else:
        symbol = symbol.title()
    number = element(symbol).atomic_number
    return number


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
