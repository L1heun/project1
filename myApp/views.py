# -*- coding: utf-8 -*-

from myApp import app
from flask import render_template, url_for, request, redirect, send_file
import json
import controllers as control

def Render(template, data = None) :
	result = control.getAccountInfo()
	result = json.loads(result)
	if result['result'] != -1 :
		return render_template(template, loginData = result, data = data)
	return render_template(template)

@app.route('/')
def index() :
	result = control.getAccountInfo()
	result = json.loads(result)
	if result['result'] != -1 :
		return redirect(url_for("home"))
	return render_template('index.html')

@app.route("/api/ver-1/user/logout")
def logout() :
	result = control.logout()
	result = json.loads(result)
	if result['result'] == 1 :
		result = redirect(url_for("index"))
	elif result['result'] == -1 :
		result = "<script>alert('로그아웃에 실패하였습니다'); history.back(-1); </script>"
	return result

@app.route('/api/ver-1/user/login', methods = ['POST'])
def login() :
	if request.method == 'POST':
		userId = request.form['inputEmail']
		userPwd = request.form['inputPassword']
		result = control.login(userId, userPwd)
		result = json.loads(result)
		if result['result'] == -1 :
			result = "<script>alert('계정 혹은 패스워드가 잘못되었습니다.'); history.back(-1); </script>"
		elif result['result'] == 1:
			result = redirect(url_for("home"))
		return result

	return redirect(url_for("home"))

@app.route('/api/ver-1/user/join', methods = ['POST'])
def join() :
	if request.method == 'POST':
		userId = request.form['inputEmail']
		userPwd = request.form['inputPassword']
		userFirstName = request.form['inputFirstName']
		userLastName = request.form['inputLastName']
		result = control.join(userId, userPwd, userFirstName, userLastName)
		result = json.loads(result)
		if result['result'] == -1 :
			result = "<script>alert('이미 존재하는 계정입니다'); history.back(-1); </script>"
		elif result['result'] == 1 :
			result = redirect(url_for("home"))
		return result

	return redirect(url_for("home"))

@app.route("/api/ver-1/file/upload", methods = ['POST'])
def fileUpload() :
	files = request.files.get('files')
	result = control.uploadFile(files)
	return json.dumps(result)

@app.route('/home')
def home() :
	result = control.getFileList()
	return Render('service/home.html', data = result)

@app.route("/download/<fileIdx>")
def download(fileIdx) :
	result = control.downloadFile(fileIdx)
	return result
