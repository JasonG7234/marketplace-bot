from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json

def send_email_old(listings):
	SUBJECT = "Best Facebook Marketplace Listings"
	FROMADDR = "variousemaillists@gmail.com"
	FROMPASSWORD = json.load(open('src/gmail/app_password.json'))['app_password']
	TOADDR = "JasonG7234@gmail.com"
	
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = SUBJECT
	MESSAGE['From'] = FROMADDR
	HTML_BODY = MIMEText(populate_email_body(listings), 'html')
	MESSAGE.attach(HTML_BODY)
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(FROMADDR, FROMPASSWORD)
	
	server.sendmail(FROMADDR, TOADDR, MESSAGE.as_string())
		
	server.quit()

from jinja2 import Template

def populate_email_body(listings):
	template = Template(open("src/gmail/email.html").read())
	return template.render(listings=listings)