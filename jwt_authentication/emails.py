import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
def send_verification_email(user, token):
    verification_link = (f"http://127.0.0.1:8000/api/verify-email/{token}"
    )

    logger.info(
        f"""
        ===================================
        EMAIL VERIFICATION
        To: {user.email}

        Please click this link:

        {verification_link}

        ===================================

        """

    )