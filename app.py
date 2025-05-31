from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/post')
def index():
    return render_template('post/index.html.jinja')

if __name__ == '__main__':
    app.run(port=5050, debug=True)
