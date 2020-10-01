import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Collect the price from amazon and send to email
def Main():
	#Include the User Agent (can be found by typing "user agent" in google, just paste that in)
	URL = 'https://www.XXXX.com/XXXX'
	headers = {"User-Agent": 'XXXX'}
	email = 'XXXX@gmail.com' #you can use your own gmail if you enable "less secure apps" on Google, it will send the email to itself
	password = 'XXXX' #your gmail password

	#collecting the price then sending an email
	title, price = collectPrice(URL, headers)
	sendMail(email, password, title, price)

def collectPrice(URL, headers):
	page = requests.get(URL, headers = headers)

	#Sometimes needs to be done twice
	contentCollector1 = BeautifulSoup(page.content, "lxml")
	contentCollector2 = BeautifulSoup(contentCollector1.prettify(), "html.parser")

	#Tags that are used on amazon
	title = contentCollector2.find(id="productTitle").get_text().strip()
	price = contentCollector2.find(id="buyNewSection").get_text().strip()

	#Formatting the price data
	price = price[price.find("$") + 1:]
	price = float(price)

	return (title, price)

def sendMail(email, password, title, price):
	#Startup server
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(email, password)
	
	#Email formatting
	subject = 'Current Price for "' + title + '"'
	body = 'This item costs $' + str(price)
	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(email,email,msg)
	server.quit()

	#print("Email has been sent")

if __name__ == '__main__':
	Main()
