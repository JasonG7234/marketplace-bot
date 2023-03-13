import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

FLOW = InstalledAppFlow.from_client_secrets_file(
            'src/gmail/credentials.json', 
            [ "https://www.googleapis.com/auth/gmail.send" ])
creds = FLOW.run_console()

def send_email(listings):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(populate_email_body(listings), 'html')
    message['to'] = 'JasonG7234@gmail.com'
    message['subject'] = 'Facebook Marketplace Deals'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

from jinja2 import Template

def populate_email_body(listings):
	template = Template(open("src/gmail/email.html").read())
	return template.render(listings=listings)