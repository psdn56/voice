from flask import Flask, request, render_template, send_file
from TTS.api import TTS

app = Flask(__name__)

# Load model once
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]

        tts.tts_to_file(
            text=text,
            speaker_wav="myvoice.wav",
            language="en",
            file_path="output.wav"
        )

        return render_template("index.html", audio=True)

    return render_template("index.html", audio=False)


@app.route("/audio")
def audio():
    return send_file("output.wav", mimetype="audio/wav")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
