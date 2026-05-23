from flask import Flask

app = Flask(__name__)

@app.get("/profile")
def profile():
    return '''
    <div id="welcome"></div>
    <script>
      const params = new URLSearchParams(location.search);
      const name = params.get("name") || "guest";
      const node = document.createElement("b");
      node.textContent = "Welcome " + name;
      document.querySelector("#welcome").replaceChildren(node);
    </script>
    '''
