from flask import Flask
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

env = Environment(loader=PackageLoader('hello', 'templates'))

@app.route("/<nome>")
def hello(nome):
    mappa = {"titolo" : nome}
    template = env.get_template("test.html")
    return template.render(titolo=nome, paragrafo="ciao")

@app.route("/a")
def route_a():
    return """<html>
    <body>
     <h1> Titolo </h1> 
     <p>paragrafo</p>
    </body>
    </html>"""

if __name__ == "__main__":
    app.run()
