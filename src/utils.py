import re

def is_valid_phone(phone):
    pattern = r"^\+7[- ]?\d{3}[- ]?\d{3}[- ]?\d{2}[- ]?\d{2}$"
    return re.match(pattern, phone) is not None

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None
