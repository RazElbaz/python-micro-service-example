from fastapi import FastAPI
import pika
import os
import json
import smtplib
from datetime import datetime, timedelta
from twilio.rest import Client
from config import settings

app = FastAPI()

publisher_queue_name = "message_queue"
email_queue_name = "email_queue"
whatsapp_queue_name = "whatsapp_queue"

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_email(subject, message, to_email):
    # connect to the SMTP server
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        # compose the email
        email_body = f"Subject: {subject}\n\n{message}"

        # send the email
        server.sendmail(settings.SMTP_USER, to_email, email_body)

def handle_text_message(body):
    # handle the text message logic here
    data = body.decode("utf-8")
    print(f"Received a text message: {data}")

def handle_email_message(body):
    try:
        # try to decode the message as JSON
        data = json.loads(body.decode("utf-8"))

        # extract email details
        subject = data.get("subject")
        message = data.get("message")
        to_email = data.get("email_to")

        # send the email
        send_email(subject, message, to_email)
        print(f"Email sent to {to_email}")

    except json.JSONDecodeError as json_error:
        # handle JSON decoding error
        print(f"Failed to decode JSON message: {json_error}")
        raise

def handle_whatsapp_message(body):
    try:
        # try to decode the message as JSON
        data = json.loads(body.decode("utf-8"))

        # extract WhatsApp details
        phone_number = data.get("whatsapp_to")
        message = data.get("message")

        # calculate the scheduled time
        now = datetime.now()
        scheduled_time = now + timedelta(hours=2, minutes=0)

        # convert the scheduled time to 24-hour format
        scheduled_time_str = scheduled_time.strftime("%H:%M")

        # send the message
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{phone_number}'
        )

        print(f"WhatsApp message sent at {scheduled_time_str} to {phone_number}.")

    except json.JSONDecodeError as json_error:
        # handle JSON decoding error
        print(f"Failed to decode JSON message: {json_error}")
        raise


def consume_text_message(ch, method, properties, body):
    try:
        handle_text_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Failed to process text message: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def consume_email_message(ch, method, properties, body):
    try:
        handle_email_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Failed to process email message: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def consume_whatsapp_message(ch, method, properties, body):
    try:
        handle_whatsapp_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Failed to process WhatsApp message: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

@app.on_event("startup")
async def startup_event():
    # this function will be executed when the FastAPI app starts
    app.rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            settings.RABBIT_HOST, int(settings.RABBIT_PORT), '/', pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
        )
    )
    app.rabbit_channel = app.rabbit_connection.channel()

    # declare queues
    app.rabbit_channel.queue_declare(queue=publisher_queue_name, durable=True)
    app.rabbit_channel.queue_declare(queue=email_queue_name, durable=True)
    app.rabbit_channel.queue_declare(queue=whatsapp_queue_name, durable=True)

    # use basic_consume for continuous message consumption
    app.rabbit_channel.basic_consume(queue=publisher_queue_name, on_message_callback=consume_text_message, auto_ack=False)
    app.rabbit_channel.basic_consume(queue=email_queue_name, on_message_callback=consume_email_message, auto_ack=False)
    app.rabbit_channel.basic_consume(queue=whatsapp_queue_name, on_message_callback=consume_whatsapp_message, auto_ack=False)

    app.rabbit_channel.start_consuming()

@app.on_event("shutdown")
async def shutdown_event():
    # this function will be executed when the FastAPI app shuts down
    app.rabbit_channel.stop_consuming()
    app.rabbit_connection.close()



