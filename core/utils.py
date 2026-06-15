import secrets
import string
import time
from datetime import datetime

class UIDGenerator:
    ALPHANUMERIC = string.ascii_letters + string.digits
    ALPHANUMERIC_SYMBOLS = string.ascii_letters + string.digits + "!@#$%&*"
    
    @classmethod
    def generate_uid(cls, length=12, use_symbols=False):
        char_set = cls.ALPHANUMERIC_SYMBOLS if use_symbols else cls.ALPHANUMERIC
        return ''.join(secrets.choice(char_set) for _ in range(length))
    
    @classmethod
    def generate_uid_with_prefix(cls, prefix, length=10, use_symbols=False):
        uid = cls.generate_uid(length, use_symbols)
        return f"{prefix}_{uid}"

# Regular functions for Django migrations (no lambdas!)
def get_org_uid():
    return UIDGenerator.generate_uid_with_prefix('ORG', 12)

def get_contact_uid():
    return UIDGenerator.generate_uid_with_prefix('CT', 12)

def get_list_uid():
    return UIDGenerator.generate_uid_with_prefix('LST', 10)

def get_tag_uid():
    return UIDGenerator.generate_uid_with_prefix('TAG', 8)

def get_template_uid():
    return UIDGenerator.generate_uid_with_prefix('TPL', 10)

def get_campaign_uid():
    return UIDGenerator.generate_uid_with_prefix('CMP', 10)

uid_generator = UIDGenerator()
