from django.core.signing import Signer, BadSignature


class SMTPPasswordService:
    @staticmethod
    def encrypt(raw_password: str) -> str:
        if not raw_password:
            return ""
        return Signer().sign(raw_password)

    @staticmethod
    def decrypt(encrypted_password: str) -> str:
        if not encrypted_password:
            return ""

        try:
            return Signer().unsign(encrypted_password)
        except BadSignature:
            return encrypted_password
