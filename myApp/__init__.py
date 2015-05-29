from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_object('config')
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.errorhandler(404)
def not_found(error) :
	return render_template('except/404.html'), 404

@app.errorhandler(405)
def method_not_allow(error) :
	return render_template('except/405.html'), 405

import myApp.views
import myApp.controllers
