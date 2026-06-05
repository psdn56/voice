from flask import Flask, render_template, request, send_file, jsonify
import os
import time

app = Flask(__name__)

# Lazy load (VERY IMPORTANT for Render)
tts = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return "OK"


@app.route("/generate", methods=["POST"])
def generate():
    global tts

    try:
        # Import TTS ONLY when needed (prevents startup crash)
        if tts is None:
            from TTS.api import TTS
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        filename = f"output_{int(time.time())}.wav"

        tts.tts_to_file(
            text=text,
            speaker_wav="voice.wav",
            language="en",
            file_path=filename
        )

        return send_file(
            filename,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="voice.wav"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# IMPORTANT for Render + Gunicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
