from passlib.hash import pbkdf2_sha256
from rest_framework.authtoken.models import Token


def hash_password(password):
    """
    Hashes a password using PBKDF2-SHA256 algorithm.
    Args:
        password (str): The password to be hashed.
    Returns:
        str: Hashed password.
    """
    try:
        return pbkdf2_sha256.hash(password)
    except Exception as e:
        return f"{e}"

def compare_hashed_passwords(attempted_password, password_from_db):
    """
    Compares an attempted password with a hashed password from the database.
    Args:
        attempted_password (str): The password attempt to be compared.
        password_from_db (str): The hashed password retrieved from the database.
    Returns:
        bool: True if the attempted password matches the hashed password, False otherwise.
    """
    try:
        return pbkdf2_sha256.verify(attempted_password, password_from_db)
    except Exception as e:
        return f"{e}"



def create_access_token(user):
    user_token = Token.objects.create(user=user)
    return user_token