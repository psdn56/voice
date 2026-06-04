from flask import Flask, render_template, request, send_file, jsonify
from TTS.api import TTS
import os
import time

app = Flask(__name__)

# Load model ONCE (important)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:
        text = request.json["text"]

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # unique file name (avoids overwrite issues)
        filename = f"output_{int(time.time())}.wav"

        # generate voice
        tts.tts_to_file(
            text=text,
            speaker_wav="voice.wav",
            language="en",
            file_path=filename
        )

        # check file
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return jsonify({"error": "Audio generation failed"}), 500

        return send_file(
            filename,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="voice.wav"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
