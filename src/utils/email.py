from ..services.email.fast_mail import send_email_background
import dotenv
import os

dotenv.load_dotenv()


def send_verification_email(email: str, verification_token: str):
    return send_email_background(
        {
            "subject": "Signup Successfull",
            "recipients": email,
            "body": f"{os.getenv("HOST_NAME")}/api/auth/verify-email?token={verification_token}",
        }
    )


def send_reset_password_email(email: str, reset_password_token: str):
    return send_email_background(
        {
            "subject": "Reset password",
            "recipients": email,
            "body": f"{os.getenv("HOST_NAME")}/api/auth/reset-password/{reset_password_token}",
        }
    )
