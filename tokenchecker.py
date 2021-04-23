#Replit Database Token Checker
#	Created by Noah St. Juliana (nstjuliana@gmail.com)
#	Checks a list of Database URLs for expiration. Executes every two minutes.
#	
#	

from bs4 import BeautifulSoup
import time
import requests
import ssl
import smtplib
from datetime import datetime

#Email Config
port = 465  # For SSL
sender_email = "s308alert@gmail.com"
receiver_email = ['nstjuliana@gmail.com', 'nstjulia@iu.edu', 'jmmejia@iu.edu']
defaultmessage = """\
Subject: Database Token Expired [IUS308]

A Database Token has been detected as invalid. Here are the details:\n\n"""

# Create a secure SSL context
context = ssl.create_default_context()

# Dictionary of URLs to Check
thisdict = {
  "Snake": "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkyNjUyMDcsImlhdCI6MTYxOTE1MzYwNywiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJiYTJkZWYxYS1jYmY3LTRmM2EtODJkMy02ZWNkNjczM2JmMDEifQ.-g0k8NXdoh-PtmiXhbETGaxChjo6RrjD4flwP8tvvL9KBL8D_ERAUCh6tMQX-e8QmBYWO8buQb9eX68QMt-1Kw",

  "2048": "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkyNjUyMTMsImlhdCI6MTYxOTE1MzYxMywiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJkMTIwZjBlOC02OGRlLTQxOWEtYTZmMS0yMjUwNTYwZTY4MjUifQ.NYtmfDJXBgTJLcUKL2PuCO95EDRMRRj_3geH85hmvFPYA_LhqNIwg96S_ug_f3U-EkR9wSnElf4JHiTtBXR_Ew",

  "Greed": "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkyNjUyMTMsImlhdCI6MTYxOTE1MzYxMywiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJlNTUxMGM3Yi1lMWJlLTQzMTQtYTZjMC01MzFjYTFhOTgzZTUifQ.Qy6z4P4w0rBk46EWs_1fwkHzIG8zgg9s_M2uG4Ft70PbKZ6gLBWtpkFjSoX_KKUUp7pXu8dNv6bf_9XHOV5JyQ",

  "Flappy Bird": "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkyNjUyMTQsImlhdCI6MTYxOTE1MzYxNCwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJjMGRjNmRlYy05ZDY3LTQwMGYtODU1NC05MTFmYTg5ZTRiODQifQ.5Z4olSibrwyAUcVNrVDyc62UlRObIDxD2EXiJHL477Jlbm7rwiQn06JMRLdT8iy-drzjz4oXjzp01Wjb-2MBmQ",
  
  "Rock Paper Scissors": "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkyNjUyMDksImlhdCI6MTYxOTE1MzYwOSwiaXNzIjoiY29ubWFuIiwiZGF0YWJhc2VfaWQiOiJhYzdjMjliZC1mODA1LTQxMzctYTM4ZS02YmZjOWVlYTFmMzcifQ.2kMkWZNAVp-ja19hZEbVczss1n2OvUHKGt5vGH6GVcRmwSKYVAbeBf0--1y1_f1xQueSQu2fiUrnDEpOtr6Ekw"
}

#Infinite loop, exit program via Ctrl+Z (Ctrl+C on Windows) or by closing console/browser
while True:
	if len(thisdict) == 0:
			print('All Tokens Expired, no URLs to check. Quitting.')
			exit()
	ExpiredGames = []
	for key, value in thisdict.items():
		#Get the current date/time
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

		print ('[' + dt_string + '] ' + 'Testing ' + key + '...')

		#Check for 'expired' in DB URL
		page = requests.get(value)

		if 'expired' in page.text:
			print('Expired! Sending Email Notifications')
			message = defaultmessage

			#Prepare and send Email Notification
			message += '[' + dt_string + '] ' + key + ': \t' + value

			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.login("s308alert@gmail.com", 'Thefutureisnow!')
			server.sendmail(sender_email, receiver_email, message)
			ExpiredGames.append(key)
			print('[' + dt_string + '] Emails Sent.')
		else:
			print('Valid!')
	 	
	 	# Delete Expired Games from Dictionary. Wait 2 minutes before relooping
	for game in ExpiredGames:
		del thisdict[game]
	time.sleep(120)