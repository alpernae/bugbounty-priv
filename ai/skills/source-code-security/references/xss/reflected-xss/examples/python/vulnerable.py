from flask import Flask, request

app = Flask(__name__)

@app.get("/search")
def search():
    query = request.args.get("q", "")
    html = f'''
      <html>
        <body>
          <h1>Search</h1>
          <p>Results for: {query}</p>
        </body>
      </html>
    '''
    return html
