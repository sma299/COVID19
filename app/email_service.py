# app/email_service.py

import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
MY_EMAIL = os.environ.get("MY_EMAIL_ADDRESS")

def send_email(subject="Test Email for COVID-19 County Data", html="<p>This was a successful email!</p>"):
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)
    message = Mail(from_email=MY_EMAIL, to_emails=MY_EMAIL, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", e.message)
        return None

if __name__ == "__main__":
    example_subject = "Test Email for COVID-19 County Data"

    # multiline string using triple quotes, also this is in HTML
    example_html = f"""
    <h3>This is a test of the COVID-19 County Data Tracker</h3>

    <h4>Today's Date</h4>
    <p>Monday, January 1, 2040</p>
    
    """

    send_email(example_subject, example_html)