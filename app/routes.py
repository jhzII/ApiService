from app import app
from flask import render_template


@app.route('/hello')
def test():
    return render_template('hello.html', name='User')
