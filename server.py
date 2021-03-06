# save this as app.py
from flask import Flask, request
from twilio.rest import Client
import os
import boto3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World Flask for notifications!"


@app.route("/email", methods=['POST'])
def email():
    hash = request.form['hash_validator']
    if(hash == "Admin12345@2022Ucaldas"):
        print(hash)
        to = request.form['destination']
        subject = request.form['subject']
        message = request.form['message']
        SENDGRID_API_KEY = "SG.L5s..."
        message = Mail(
            from_email="origeno@ucaldas.edu.co",
            to_emails=to,
            subject=subject,
            html_content=message)
        try:
            sg = SendGridAPIClient(os.environ.get(SENDGRID_API_KEY))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
    else:
        return "hash_error"


@app.route("/sms", methods=['POST'])
def sms():
    hash = request.form['hash_validator']
    if(hash == "Admin12345@2022Ucaldas"):
        destination = request.form['destination']
        message = request.form['message']
        client = "aws"
        if(client == "aws"):
            # Create an SNS client
            client = boto3.client(
                "sns",
                aws_access_key_id=os.environ["aws_access_key_id"],
                aws_secret_access_key=os.environ["aws_secret_access_key"],
                region_name="us-east-1"
            )

            # Send your sms message.
            client.publish(
                PhoneNumber=destination,
                Message=message
            )
        else:
            try:
                account_sid = os.environ["account_sid"]
                auth_token = os.environ["auth_token"]
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    messaging_service_sid=os.environ["messaging_service_sid"],
                    body=message,
                    to=destination
                )
                print(message.sid)
                return "OK"
            except:
                return "KO"
    else:
        return "hash_error"


if __name__ == '__main__':
    app.run()
