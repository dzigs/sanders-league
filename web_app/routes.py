from flask import render_template
from web_app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'dzigs'}
    return render_template('index.html', title='Test', user=user)
