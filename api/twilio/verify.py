import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv("config/.env")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SERVICE = os.environ.get("TWILIO_VERIFY_SERVICE")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_verification(to_email):
    client.verify.services(TWILIO_VERIFY_SERVICE).verifications.create(to=to_email, channel="email")


def check_verification_token(to_email, token):
    check = client.verify.services(TWILIO_VERIFY_SERVICE).verification_checks.create(to=to_email, code=token)
    return check.status == "approved"
