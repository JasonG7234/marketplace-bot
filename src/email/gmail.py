import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

FLOW = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', [ "https://www.googleapis.com/auth/gmail.send" ])
creds = FLOW.run_local_server(port=8081)

def send_email(data):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(data)
    message['to'] = 'JasonG7234@gmail.com'
    message['subject'] = 'Facebook Marketplace Deals'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None
'''
	SUBJECT = "BearDown Stats HTML"
	FROMADDR = "variousemaillists@gmail.com"
	FROMPASSWORD = "***" 
	TOADDR = ['JasonG7234@gmail.com']
	
	MESSAGE = MIMEMultipart('alternative')
	MESSAGE['subject'] = SUBJECT
	MESSAGE['From'] = FROMADDR

	HTML_BODY = MIMEText(data, 'html') #Record MIME type text/html
	MESSAGE.attach(HTML_BODY)
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(FROMADDR, FROMPASSWORD)
	
	for email in TOADDR:
		MESSAGE['To'] = email
		server.sendmail(FROMADDR, [email], MESSAGE.as_string())
		
	server.quit()
'''