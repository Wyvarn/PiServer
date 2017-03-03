"""
The email confirmation should contain a unique URL that a user simply needs to click in order to confirm his/her account.
Ideally, the URL should look something like this – http://<domain-name>/confirm/<id>.
The key here is the id. We are going to encode the user email (along with a timestamp) in the id using the
itsdangerous package.
"""

from itsdangerous import URLSafeSerializer
from flask import current_app


def generate_token(email):
    """
    generates a confirmation token for the user to click on to confirm their token
    the email will be encoded in the token
    :param email: user's email
    :return: confirmation token for the user to use
    """
    serializer = URLSafeSerializer(secret_key=current_app.config.get("SECRET_KEY"))
    return serializer.dumps(email, salt=current_app.config.get("SECURITY_PASSWORD_SALT"))


# todo: set the expiration time for token
def confirm_token(token, expiration=7200):
    """
    This is used to confirm the user token used to confirm user email.
    :param token: the token sent to the user email
    :param expiration: how long before this token expires
    :return: the user email
    :rtype: str
    """
    serializer = URLSafeSerializer(current_app.config.get("SECRET+KEY"))
    try:
        email = serializer.loads(
            token,
            salt=current_app.config.get("SECURITY_PASSWORD_SALT")
        )
    except Exception as e:
        print("Confirm token error: ", e)
        return False
    return email
