from flask import *
from API import apiBlueprint

app=Flask(__name__,static_folder="layout", static_url_path="/layout")
app.register_blueprint(apiBlueprint)
app.secret_key="123456"
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/movie/<id>")
def movie(id):
	return render_template("movie.html")
@app.route("/search")
def search():
	return render_template("search.html")
@app.route("/login")
def login():
	return render_template("login.html")
@app.route("/favorite")
def favorite():
	return render_template("favorite.html")

app.run(host='0.0.0.0',port=3000)