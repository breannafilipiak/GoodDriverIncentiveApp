from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class Create_Account_Token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + 
            text_type(user.is_active)
        )

activate_account = Create_Account_Token()
