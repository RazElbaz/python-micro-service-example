# Messaging Microservice

This repository contains a  Python-based API microservice designed to serve as an interface between the system and external communication channels. The primary focus of this API is to handle and process messages originating from different sources, including text messages, email messages, and WhatsApp messages.


## Input and Output

### Input

The messaging microservice accepts messages from various channels, including text messages, email messages, and WhatsApp messages. The input messages are sent to the microservice through a RabbitMQ message broker. Each type of message (text, email, WhatsApp) is routed to the microservice using specific routing keys.

#### Supported Message Types:

1. **Text Message:**
   - **Routing Key:** `text_message`
   - **Input Format:** Plain text message.

2. **Email Message:**
   - **Routing Key:** `email_message`
   - **Input Format:** JSON payload conforming to the `EmailMessagereceived` schema.

3. **WhatsApp Message:**
   - **Routing Key:** `whatsapp_message`
   - **Input Format:** JSON payload conforming to the `WhatsappMessagereceived` schema.

### Output

The microservice processes the input messages and performs the following actions based on the message type:

1. **Text Message:**
   - Logs the received text message.

2. **Email Message:**
   - Sends an email with the specified subject, message, and optional attachment to the recipient email address.

3. **WhatsApp Message:**
   - Sends a WhatsApp message with the specified content and optional media attachment to the specified phone number.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system.

### Installation and Setup

Build the Docker image:

```bash
docker build -t messaging-microservice .
```

### Environment Configuration

Create a `.env` file in the root directory and set the following environment variables:

```env
RABBIT_HOST=your-rabbit-host
RABBIT_PORT=your-rabbit-port
RABBIT_USERNAME=your-rabbit-username
RABBIT_PASSWORD=your-rabbit-password

SMTP_HOST=your-smtp-host
SMTP_PORT=your-smtp-port
SMTP_USER=your-smtp-username
SMTP_PASSWORD=your-smtp-password

TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

AWS_BUCKET_NAME=your-aws-bucket-name
AWS_ACCESS_KEY=your-aws-access-key
AWS_SECRET_KEY=your-aws-secret-key
AWS_REGION=your-aws-region
```

### Usage

1. Create a Docker network for RabbitMQ:

   ```bash
   docker network create rabbits
   ```

2. Run RabbitMQ container:

   ```bash
   docker run -d --rm --net rabbits -p 8080:15672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8
   ```

3. Build and run the messaging microservice container:

   ```bash
   docker build -t messaging-microservice .
   docker run -it --rm --net rabbits -p 80:8080 messaging-microservice
   ```

## Directory Structure

- **app/**: Contains the microservice implementation files.
  - **handlers/**: Message handling logic for different message types.
  - **senders/**: Modules for sending messages through email and WhatsApp.
  - **templates/**: Message templates for email and WhatsApp.
  - **utils/**: Utility modules, including rmq, logger and aws.
- **test.py**: Test cases for ensuring proper functionality.
- **.env**: Environment variable configuration file.
- **Dockerfile**: Docker configuration file for building the microservice image.
- **pyproject.toml**: Poetry configuration file.

## Running Tests

### Test Execution

To run the tests and ensure proper functionality, use the following command:

```bash
pytest -p no:warnings tests/test.py
```

The `-p no:warnings` option suppresses unnecessary warnings during test execution.

### Running the Test Publisher

If you want to test the publisher functionality separately, you can use the `test_publisher` located in the `tests/test_publisher` directory. Follow these steps to build and run the `test_publisher` Docker container:

#### Navigate to the Test Publisher Directory

```bash
cd ./tests/test_publisher/
```

#### Build the Docker Image

```bash
docker build -t publisher .
```

#### Run the Docker Container

```bash
docker run -it --rm --net rabbits -p 81:8080 publisher
```

This will build the Docker image for the `test_publisher` and run it in a container. Ensure that you have the RabbitMQ server running and the necessary environment variables configured as mentioned in the main README.

