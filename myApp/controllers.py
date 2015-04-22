from flask import session, redirect, url_for, render_template, flash, g

def login(userId, userPwd) :
	print "userId : %s, userPwd : %s" % (userId, userPwd)
	return 1;

def join(userId, userPwd, userFirstName, userLastName) :
	print "userId : %s, userPwd : %s, userFirstName : %s, userLastName : %s" % (userId, userPwd, userFirstName, userLastName)
	return 1;	