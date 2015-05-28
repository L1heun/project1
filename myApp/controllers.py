# -*- coding: utf-8 -*-

from flask import session, redirect, url_for, render_template, flash, g, request, send_file
import models as model
import time, random, os, datetime
import hashlib, json
from werkzeug import secure_filename
import sys
reload(sys)  
sys.setdefaultencoding('utf-8')

UPLOAD_FOLDER = "myApp/static/media"
MUSIC_EXT = ['mp3', 'wma', 'wmv', 'mid']
MOVIE_EXT = ['mp4', 'avi', 'mpeg', 'mov', 'flv']
IMAGE_EXT = ['jpg', 'bit', 'png', 'ai', 'psd', 'svg']


def getFileList() :
	if 'userToken' in session :
		entries = list()
		userIdx = model.getAccountByToken(session['userToken'])[0][0]
		sql = "SELECT file_idx, folder_idx, file_origin_name, file_type, folder_init_date, file_path "
		sql += "FROM files where user_idx = %s" % (userIdx)
		result = model.query(sql)
		if result :
			for i in result :
				entry = dict()
				entry['fileIdx'] = i[0]
				entry['folderIdx'] = i[1]
				entry['fileOriginName'] = i[2]
				entry['fileType'] = i[3]
				entry['fileInitDate'] = i[4].strftime("%Y/%m/%d %H시  %M분")
				entry['filePath'] = i[5].split("/", 1)[1]
				print i
				entries.append(entry)
			return entries
		return None

def tokenIssue(userIdx) :
	t = time.time()
	hashObj = hashlib.sha384(str(userIdx) + str(int(t)) + str(random.randrange(1, 1000)))
	hashData = hashObj.hexdigest()
	hashObj = hashlib.md5(hashData)
	token = hashObj.hexdigest()
	return token

def passwdEncrypt(pwd) :
	hashObj = hashlib.sha384(pwd)
	result = hashObj.hexdigest()
	return result

def logout() :
	if 'userToken' in session :
		userIdx = model.getAccountByToken(session['userToken'])[0][0]
		session.clear()
		model.updateToken(userIdx)
		return json.dumps({"result" : 1})
	return json.dumps({"result" : -1})

def login(userId, userPwd) :
	userPwd = passwdEncrypt(userPwd)
	result = model.getAccount(userId, userPwd)

	if result[0][0] == 1 :
		userIdx = result[0][1]
		token = tokenIssue(userIdx)
		userToken = model.updateToken(userIdx,token)[0][0]
		session['userToken'] = userToken
		return json.dumps({"result" : 1})

	return json.dumps({"result" : -1})

def join(userId, userPwd, userFirstName, userLastName) :
	userPwd = passwdEncrypt(userPwd)
	identifyAccount = model.getAccount(userId, userPwd)

	if identifyAccount[0][0] == 0 :
		userNickName = userFirstName + " " + userLastName
		result = model.appendAccount(userId, userPwd, userNickName)
		token = tokenIssue(result)
		userToken = model.updateToken(result,token)[0][0]
		session['userToken'] = userToken
		return json.dumps({"result" : 1})

	return json.dumps({"result" : -1})

def getAccountInfo() :
	if 'userToken' in session :
		account = model.getAccountByToken(session['userToken'])
		return json.dumps({"result" : account})
	else :
		return json.dumps({"result" : -1})

def uploadFile(files) :
	if 'userToken' in session :
		userIdx = model.getAccountByToken(session['userToken'])[0][0]
		folder = os.path.join(UPLOAD_FOLDER, str(userIdx))
		if not os.access(folder, os.F_OK) :
			os.mkdir(folder)
		fileExt = files.filename.rsplit('.', 1)[1].lower()
		if fileExt in MUSIC_EXT :
			fileExt = 'music'
		elif fileExt in MOVIE_EXT :
			fileExt = 'movie'
		elif fileExt in IMAGE_EXT :
			fileExt = 'image'
		else :
			fileExt = 'file'
		fileName = secure_filename(files.filename)
		filePath = os.path.join(folder, str(int(time.time())))
		dbFilePath = filePath.split("/", 1)[1]
		files.save(filePath)
		nTime = datetime.datetime.fromtimestamp(time.time())
		sql = "SELECT folder_idx FROM folder WHERE user_idx = %s order by folder_idx asc" % (userIdx)
		result = model.query(sql)
		if not result :
			sql = "INSERT INTO folder(user_idx, folder_name, folder_init_date) "
			sql += "VALUES (%s, 'index', '%s')" % (userIdx, nTime)
			model.query(sql)
		sql = "INSERT INTO files(user_idx, folder_idx, file_origin_name, file_path, file_type, file_is_shared, folder_init_date)"
		sql += "VALUES (%s, %s, '%s', '%s', '%s', %s, '%s')" % (userIdx, result[0][0], fileName, dbFilePath, fileExt, 0, nTime)
		result = model.query(sql)

		return json.dumps({"result" : 1})
	return json.dumps({"result" : -1})



def downloadFile(fileIdx) :
	if 'userToken' in session :
		userIdx = model.getAccountByToken(session['userToken'])[0][0]
		sql = "SELECT file_origin_name, file_path FROM files WHERE user_idx = %s and file_idx = %s" % (userIdx, fileIdx)
		result = model.query(sql)
		if result :
			return send_file(result[0][1], as_attachment = True, attachment_filename = result[0][0]), 200
		return "No Data", 404
	return "Permission Denied", 401














