from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
import numpy as np
import cv2
import base64
from PIL import Image
import io

# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)
CORS(app)

def read_image(base64_image):
    image_data = base64.b64decode(base64_image.split(",")[1])
    image = Image.open(io.BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        data = request.get_json()
        image = read_image(data["image"])
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        lines = text.split("\n")
        medicine_name = ""
        qty = 0
        for line in lines:
            if len(line.strip()) > 3 and medicine_name == "":
                medicine_name = line.strip()
            if any(c.isdigit() for c in line):
                numbers = [int(s) for s in line.split() if s.isdigit()]
                if numbers:
                    qty = max(qty, max(numbers))
        return jsonify({"name": medicine_name, "qty": qty})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
