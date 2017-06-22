from flask_mail import Message
from flask import current_app
from server.app import mail


def send_mail(to, subject, template):
    """
    Sends a new confirmation email to the registering user
    :param to: which email address to send to
    :param subject: the subject of the email
    :param template: the template to use.
    """
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    mail.send(msg)
