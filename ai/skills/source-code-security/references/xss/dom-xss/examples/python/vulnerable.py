from flask import Flask

app = Flask(__name__)

@app.get("/profile")
def profile():
    return '''
    <div id="welcome"></div>
    <script>
      const params = new URLSearchParams(location.search);
      const name = params.get("name") || "guest";
      document.querySelector("#welcome").innerHTML = "<b>Welcome " + name + "</b>";
    </script>
    '''
