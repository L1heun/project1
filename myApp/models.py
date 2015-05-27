# -*- coding: utf-8 -*-

import MySQLdb
import time, random

def getConnection():
	db = MySQLdb.connect(host='localhost', user='sCloud', passwd='sCloudBiz', db='scloud')
	db.set_character_set('utf8')
	return db

def getCursor(db):
	cur = db.cursor()
	cur.execute("SET NAMES utf8")
	return cur

def query(sql) :
	db = getConnection()
	cur = getCursor(db)
	cur.execute(sql)
	result = cur.fetchall()
	db.commit()
	db.close()
	return result

def logout(userToken) :
	sql = "UPDATE user_account SET user_token = '' WHERE user_token = '%s'" % (userToken)
	query(sql)
	return 1

def appendAccount(userId, userPwd, userNickName) :
	t = time.localtime()
	signupTime = '%04d-%02d-%02d %02d:%02d:%02d' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
	userAccount = (userId, userPwd, userNickName, signupTime)
	sql = "INSERT INTO user_account(user_id, user_passwd, user_nick_name, user_signup_time) VALUES('%s', '%s', '%s', '%s')" % userAccount
	query(sql)

	sql = "SELECT user_idx FROM user_account WHERE user_id = '%s' and user_passwd = '%s'" % (userId, userPwd)
	result = query(sql)
	return result[0][0]

def getAccount(userId, userPwd) :
	sql = "SELECT count(user_idx), user_idx FROM user_account WHERE user_id = '%s' and user_passwd = '%s'" % (userId, userPwd)
	result = query(sql)
	return result

def getAccountByToken(userToken) :
	sql = "SELECT user_idx, user_nick_name FROM user_account WHERE user_token = '%s'" % (userToken)
	result = query(sql)
	return result

def updateToken(userIdx, userToken=None) :
	print str(userIdx) + " : " + str(userToken)
	if userToken : 
		sql = "UPDATE user_account SET user_token = '%s' where user_idx = %d" % (userToken, userIdx)
	else :
		sql = "UPDATE user_account SET user_token = NULL WHERE user_idx = %d" % (userIdx)
	query(sql)
	sql = "SELECT user_token FROM user_account WHERE user_idx = %d" % (userIdx)
	result = query(sql)
	return result