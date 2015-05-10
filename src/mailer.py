#!/usr/bin/python
# -*-coding:Latin-1 -*
# Developped By : Abdelli Haithem & Bessaad Firas
import smtplib
import getpass

import mimetypes
import email
import email.mime.application

msg = email.mime.Multipart.MIMEMultipart()

# mail + password
gmail_user =  raw_input('enter your gmail : ')
gmail_pwd = getpass.getpass('enter your password : ')

# collect emails from emails.txt  # TO = list of emails
error = True
while error == True:
	try:
		emails_path = raw_input('enter path to emails txt file : ')
		with open (emails_path, "r") as emails_file:
			emails = emails_file.read()
			TO = emails.split("\n")
			error = False
	except:
		print "unvalid path"

# msg subject
subject = raw_input('enter your email subject (exp : Stage) : ')
msg['Subject'] = subject
# msg sender
msg['From'] = gmail_user
# msg body
error = True
while error == True:
	try:	
		content_path = raw_input('enter path to message content txt file : ')	
		with open (content_path, "r") as content:
			TEXT = content.read()
    			body = email.mime.Text.MIMEText(TEXT)
			msg.attach(body)
			error = False
	except:
		print "unvalid path"
# msg cv attachment
error = True
while error == True:
	try:
		filename = raw_input('enter path to your cv : ') 
		fp=open(filename,'rb')
		att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
		fp.close()
		att.add_header('Content-Disposition','attachment',filename=filename)
		msg.attach(att)
		error = False
	except:
		print "unvalid path"

#begin
try:
	#connect to server	
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	#connect gmail account
	try:
		server.login(gmail_user, gmail_pwd)
		print "Login succesfully"
	except:
		print "Failed to login, verify your email and password"
	#send separatly emails
	for email in TO:
		msg['To'] = email
		print "sending to : " + email
		try:	
			#send email
			server.sendmail(email,[email], msg.as_string())
			print 'successfully sent the mail to : ' + email
			del msg['To']
		except:
			#error
			print 'failed sending the mail to : ' + email
	#close server
	server.close()
except:
	print "Error"
