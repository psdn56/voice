from flask import Flask, render_template, request, send_file
from TTS.api import TTS

app = Flask(__name__)

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():

    text = request.json["text"]

    tts.tts_to_file(
        text=text,
        speaker_wav="voice.wav",
        language="en",
        file_path="output.wav"
    )

    return send_file(
        "output.wav",
        mimetype="audio/wav",
        as_attachment=False
    )

if __name__ == "__main__":
    app.run(debug=True)
