from flask import Flask, request, render_template_string
from markupsafe import escape

app = Flask(__name__)

@app.get("/search")
def search():
    query = request.args.get("q", "")
    html = '''
      <html>
        <body>
          <h1>Search</h1>
          <p>Results for: {{ query }}</p>
        </body>
      </html>
    '''
    return render_template_string(html, query=escape(query))
