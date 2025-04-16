import re
from django.core.exceptions import ValidationError


def validate_username(value):
    """Ensures username contains only allowed characters."""
    if len(value)<8:
        raise ValidationError("Username should be 8 characters long")
    if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
        raise ValidationError("Username can only contain letters, numbers, and _ . -")
    if value.isnumeric():
        raise ValidationError("Username cannot be entirely numeric.")
    return value

def validate_password(value):
    """Ensures password meets security requirements."""
    
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "Password must be at least 8 characters long, include 1 uppercase letter, 1 number, and 1 special character."
        )
    return value
