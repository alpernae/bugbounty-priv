from flask import Flask, request, jsonify
from pathlib import Path
import shutil
import zipfile

app = Flask(__name__)
DEST = Path("var/imports").resolve()

@app.post("/import")
def import_zip():
    archive = zipfile.ZipFile(request.files["file"].stream)
    for item in archive.infolist():
        target = (DEST / item.filename).resolve()
        if target == DEST or DEST not in target.parents:
            continue
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(item) as src, target.open("xb") as dst:
            shutil.copyfileobj(src, dst)
    return jsonify({"imported": True})
