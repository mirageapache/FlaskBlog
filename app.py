from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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

    print(title, content)

    # create post in db
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(port=5050, debug=True)
