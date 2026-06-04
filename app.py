from flask import Flask, render_template, request, send_file, jsonify
from TTS.api import TTS
import os
import time

app = Flask(__name__)

# Load model once (IMPORTANT for speed)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:
        text = request.json["text"]

        # Unique filename (prevents caching issues)
        output_file = f"output_{int(time.time())}.wav"

        # Generate speech
        tts.tts_to_file(
            text=text,
            speaker_wav="voice.wav",
            language="en",
            file_path=output_file
        )

        # Check if file is created properly
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            return jsonify({"error": "Audio generation failed"}), 500

        return send_file(
            output_file,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="voice.wav"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
