import os
from pathlib import Path
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

from .helpers import generate_anki, parse_text_file_to_words

UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
ALLOWED_EXTENSIONS = {"txt"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/examples")
def examples():
    return render_template("examples.html")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploads_path = (
            Path(os.path.dirname(os.path.realpath(__file__)))
            / app.config["UPLOAD_FOLDER"]
        )
        downloads_path = (
            Path(os.path.dirname(os.path.realpath(__file__)))
            / app.config["DOWNLOAD_FOLDER"]
        )

        deck_name = request.form.get("deck_name")
        # check if the post request has the file part
        if not deck_name:
            return render_template("index.html", text="Please provide deck name")
        if "file" not in request.files:
            return render_template("index.html", text="Please select a file")
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", text="Please select a file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = uploads_path / filename
            file.save(file_path)
            anki_file = f"{deck_name}.apkg"
            words = parse_text_file_to_words(file_path)
            problematic_words = generate_anki(
                deck_name, words, downloads_path / anki_file
            )
            return render_template(
                "index.html",
                problematic_words=problematic_words,
                link_to_file=f"downloads/{anki_file}",
                file_name=anki_file,
            )
    return render_template("index.html")


@app.route("/downloads/<name>")
def download_file(name):
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)
