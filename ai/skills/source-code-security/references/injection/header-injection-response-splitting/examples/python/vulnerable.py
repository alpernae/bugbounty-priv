from flask import Flask, request, Response

app = Flask(__name__)

@app.get("/download")
def download():
    filename = request.args.get("name", "report.csv")
    response = Response("id,total\n1,42\n", mimetype="text/csv")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
