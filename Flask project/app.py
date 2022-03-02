from datetime import timedelta
from flask import Flask, redirect, render_template, url_for, flash
from admin.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix = "/admin")
app.secret_key = "super key"
app.permanent_session_lifetime = timedelta(days=365)

@app.route('/')
def index():
    flash("hello you!", "alert")
    return render_template('index.html', content = ['tim','tom','tam'])

@app.route('/test')
def test():
    return redirect(url_for("user",name = "test"))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user = name)

if(__name__ == "__main__"):
    app.run(debug=True)
