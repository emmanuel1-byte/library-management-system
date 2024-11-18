from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
import dotenv
import asyncio
from ...utils.logger import logger

dotenv.load_dotenv()
import os

config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("GOOGLE_USER"),
    MAIL_PASSWORD=os.getenv("GOOGLE_PASSWORD"),
    MAIL_FROM=os.getenv("GOOGLE_USER"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(data: dict):
    email = data.get("recipients")
    recipients = [email] if isinstance(email, str) else []

    try:
        message = MessageSchema(
            subject=data.get("subject"),
            recipients=recipients,
            body=data.get("body"),
            subtype=MessageType.plain,
        )

        fm = FastMail(config)
        await fm.send_message(message)

        logger.info("Email has been sent")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return None


def send_email_background(data: dict):
    """_summary_

       Handles sending emails asynchronously in a background task.
    Creates a new event loop to run the async send_email function since background tasks run in a separate thread.

    Args:
        data (dict): Dictionary containing email data with keys:
            - recipients (str): Email address of the recipient
            - subject (str): Subject line of the email
            - body (str): Body content of the email

    Implementation:
        1. Creates new event loop for async operations in background thread
        2. Sets the created loop as the current event loop
        3. Runs the async send_email function to completion
        4. Ensures proper cleanup by closing the loop in finally block

    Note:
        - This is a synchronous wrapper around the async send_email function
        - Used as a background task to avoid blocking the main API response
        - Event loop handling is required because background tasks run in a different thread

    """

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(send_email(data))
    finally:
        loop.close()
