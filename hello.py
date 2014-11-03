from flask import Flask, request
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

env = Environment(loader=PackageLoader('hello', 'templates'))

@app.route("/logout")
def login()
    name = request.args.get('name')

@app.route("/show-login")
def show_login():
    template = env.get_template("example_form.html")
    return template.render()

@app.route("/show-form")vdfnaeò htaò ocòwxrmò
def show_form():
    template = env.get_template("simple_form.html")
    return template.render()

@app.route("/form", methods=["POST"])
def form():
    if request.method == "POST":
        print request.form["name"], request.form["pass"]
        return "The passowrd is " + request.form["pass"] + " and the name is " + request.form["name"]
    return "Error you need a POST request"

@app.route("/<nome>")
def hello(nome):
    mappa = {"titolo" : nome}
    template = env.get_template("test.html")
    return template.render(titolo=nome, paragrafo="ciao")

@app.route("/a")
def route_a():
    return """<html>
    <body> #fgsbrwec\rxqzciao
     <h1> Titolo </h1> 
     <p>paragrafo</p>
    </body>
    </html>"""

if __name__ == "__main__":
    app.run()
