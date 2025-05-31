from flask import Flask, render_template, redirect, url_for, request
import os
from config.settings import db
from flask_migrate import Migrate
from models import Post
from flask import flash
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ROOT_PATH}/db/blog.db"

db.init_app(app)
Migrate(app, db)

# 首頁
@app.route('/')
@app.route('/posts')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('posts/index.html.jinja', posts=posts)

# 新增文章(頁面)
@app.route("/posts/new")
def new():
    return render_template("posts/new.html.jinja")

# 新增文章(功能)
@app.route("/posts/create", methods=["POST"])
def create():
    title = request.form.get("title")
    content = request.form.get("content")

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit() # 寫入資料庫

    flash("文章已新增")
    return redirect(url_for("index"))

# 檢視文章詳細內容(頁面)
@app.route("/posts/<int:id>")
def detail(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/detail.html.jinja", post=post)

# 編輯文章(頁面)
@app.route("/posts/<int:id>/edit")
def edit(id):
    post = Post.query.get_or_404(id)
    return render_template("posts/edit.html.jinja", post=post)

# 編輯文章(功能)
@app.route("/posts/<int:id>/update", methods=["POST"])
def update(id):
    post = Post.query.get_or_404(id)

    post.title = request.form.get("title")
    post.content = request.form.get("content")

    db.session.add(post)
    db.session.commit()

    flash("文章更新成功！")
    return redirect(url_for("detail", id=id))

# 刪除文章(功能)
@app.route("/posts/<int:id>/delete", methods=["POST"])
def delete(id):
    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    flash("文章已刪除")
    return redirect(url_for("index"))

# 404錯誤處理
@app.errorhandler(404)
def page_not_found(e):
    return render_template("common/404.html.jinja"), 404

if __name__ == '__main__':
    app.run(port=5050, debug=True)
