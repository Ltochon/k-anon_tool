from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', content = ['tim','tom','tam'])

@app.route('/test')
def test():
    return redirect(url_for("user",name = "test"))

@app.route('/user/<name>')
def user(name):
    return f'hello {name}'

if(__name__ == "__main__"):
    app.run(debug=True)
