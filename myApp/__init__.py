from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.errorhandler(404)
def not_found(error) :
	return render_template('404.html'), 404

import myApp.views
import myApp.controllers
