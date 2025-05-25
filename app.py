# app.py
from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("base")  # you can use "small" or "medium" too

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filepath = os.path.join("temp", file.filename)
    file.save(filepath)

    try:
        result = model.transcribe(filepath)
        return jsonify({'transcript': result['text']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
