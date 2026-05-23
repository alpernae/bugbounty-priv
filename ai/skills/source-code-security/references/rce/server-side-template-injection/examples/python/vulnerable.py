from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.post("/email/preview")
def preview_email():
    template = request.form.get("template", "Hello {{ name }}")
    name = request.form.get("name", "customer")
    return render_template_string(template, name=name)
