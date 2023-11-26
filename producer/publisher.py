from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import pika
import os
import json
from config import settings

app = FastAPI()

def publish_message(queue_name: str, data: dict):
    try:
        credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
        parameters = pika.ConnectionParameters(settings.RABBIT_HOST, int(settings.RABBIT_PORT), '/', credentials)


        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                content_type='application/json',
            )
        )

        print(f"Message added to the {queue_name} queue")

        connection.close()

    except pika.exceptions.AMQPError as amqp_error:
        raise HTTPException(status_code=500, detail=f"Failed to publish message to {queue_name} queue: {str(amqp_error)}")

@app.post("/publish/{message}", response_class=PlainTextResponse)
async def publish(message: str):
    try:
        data = {"message": message}
        publish_message("message_queue", data)
        return "Message published successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {str(e)}")

@app.post("/send_email/{email}/{subject}/{message}", response_class=PlainTextResponse)
async def send_email(subject: str, message: str, email: str):
    try:
        data = {"email_to": email, "subject": subject, "message": message}
        publish_message("email_queue", data)
        return "Email message published successfully"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish email message: {str(e)}")
    
@app.post("/send_whatsapp/{phone_number}/{message}", response_class=PlainTextResponse)
async def send_whatsapp(phone_number: str, message: str):
    try:
        data = {"whatsapp_to": phone_number, "message": message}
        publish_message("whatsapp_queue", data)
        return "WhatsApp message published successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish WhatsApp message: {str(e)}")
