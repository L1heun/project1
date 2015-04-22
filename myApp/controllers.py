# -*- coding: utf-8 -*-

from flask import session, redirect, url_for, render_template, flash, g, request
import models as model
import time, random
import hashlib, json

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
