from django.conf import settings
from django.core.mail import send_mail
# import logging

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
def send_verification_email(user, token):
    verification_link = (f"{settings.FRONTEND_URL}"
                        f"/verify-email/?token={token}"
                        )
    subject = "Verify your email address"
    body = f"""
    Hello {user.first_name or user.username}, 
    Please verify your email by clicking below:
    
    {verification_link}

    This link expires in 
    {settings.EMAIL_VERIFICATION_EXPIRY_HOURS}
    hours.
    """.strip()

    send_mail(subject=subject, message=body, from_email=None, recipient_list=[user.email])

    # logger.info(
        # f"""
        # ===================================
        # EMAIL VERIFICATION
        # To: {user.email}

        # Please click this link:

        # {verification_link}

        # ===================================

        # """

    # )