from django.conf import settings
from django.core.mail import send_mail

def send_password_reset_email(user, token):
    reset_link = (f"{settings.FRONTEND_URL}"
                        f"/reset-password/?token={token}"
                        )
    subject = "Reset your password"
    body = f"""
    Hello {user.first_name or user.username}, 
    Reset your password by clicking link below:
    
    {reset_link}

    This link expires in 
    {settings.EMAIL_VERIFICATION_EXPIRY_HOURS}
    hours.
    """.strip()

    send_mail(subject=subject, message=body, from_email=None, recipient_list=[user.email])
