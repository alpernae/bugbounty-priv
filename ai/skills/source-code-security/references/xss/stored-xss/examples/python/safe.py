from flask import Flask, request, redirect
from markupsafe import escape

app = Flask(__name__)
comments = []

@app.post("/comments")
def save_comment():
    comments.append({
        "author": request.form.get("author", "anon"),
        "body": request.form.get("body", "")
    })
    return redirect("/comments")

@app.get("/comments")
def list_comments():
    rows = []
    for item in comments:
        rows.append(f"<article><b>{escape(item['author'])}</b><p>{escape(item['body'])}</p></article>")
    return "<main>" + "\n".join(rows) + "</main>"
