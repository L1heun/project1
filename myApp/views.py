from myApp import app
from flask import render_template, url_for, request
import json
import controllers as control

@app.route('/')
def index() :
	return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login() :
	if request.method == 'POST':
		userId = request.form['inputEmail']
		userPwd = request.form['inputPassword']
		result = control.login(userId, userPwd)
		return json.dumps(result)

	return render_template('account/login.html')

@app.route('/join', methods = ['POST', 'GET'])
def join() :
	if request.method == 'POST':
		userId = request.form['inputEmail']
		userPwd = request.form['inputPassword']
		userFirstName = request.form['inputFirstName']
		userLastName = request.form['inputLastName']
		result = control.join(userId, userPwd, userFirstName, userLastName)
		return json.dumps(result)

	return render_template('account/join.html')