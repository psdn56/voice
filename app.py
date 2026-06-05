from flask import Flask, render_template, request, send_file, jsonify
import os
import time

app = Flask(__name__)
tts = None

# IMPORTANT: don't load model at startup (prevents Render freeze)
tts = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    global tts

    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Load model only when first request comes
        if tts is None:
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        filename = f"output_{int(time.time())}.wav"

        tts.tts_to_file(
            text=text,
            speaker_wav="voice.wav",
            language="en",
            file_path=filename
        )

        if not os.path.exists(filename):
            return jsonify({"error": "Audio generation failed"}), 500

        return send_file(
            filename,
            mimetype="audio/wav",
            as_attachment=False,
            download_name="voice.wav"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# REQUIRED for Render + Gunicorn compatibility
if __name__ != "__main__":
    import gunicorn  # just ensures server mode

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
