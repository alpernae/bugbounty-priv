from flask import Flask, request, render_template_string

app = Flask(__name__)
TEMPLATES = {
    "welcome": "Hello {{ name }}",
    "reminder": "Reminder for {{ name }}"
}

@app.post("/email/preview")
def preview_email():
    key = request.form.get("templateKey", "welcome")
    template = TEMPLATES.get(key, TEMPLATES["welcome"])
    name = request.form.get("name", "customer")
    return render_template_string(template, name=name)
