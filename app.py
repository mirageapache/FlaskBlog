from flask import Flask, render_template, redirect, url_for, request
import os
from config.settings import db
from flask_migrate import Migrate
import models
from flask import flash
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ROOT_PATH}/db/blog.db"

db.init_app(app)
Migrate(app, db)

@app.route('/')
@app.route('/post')
def index():
    return render_template('posts/index.html.jinja')

@app.route("/posts/new")
def new():
    return render_template("posts/new.html.jinja")

@app.route("/posts/create", methods=["POST"])
def create():
    title = request.form.get("title")
    content = request.form.get("content")

    post = models.Post(title=title, content=content)
    db.session.add(post)
    db.session.commit() # 寫入資料庫

    flash("文章已新增")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(port=5050, debug=True)
