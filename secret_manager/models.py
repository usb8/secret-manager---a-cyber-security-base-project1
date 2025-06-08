from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Fix A3:2017-Sensitive Data Exposure (Encrypt the secret_key before saving)
from cryptography.fernet import Fernet, InvalidToken
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
FERNET_KEY = os.environ.get(
    'SECRET_MANAGER_KEY', Fernet.generate_key()
)  # Should store encryption key in environment variable for security
cipher_suite = Fernet(FERNET_KEY)


class Secret(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    secret_header = models.TextField(null=True, blank=True)
    secret_key = (
        models.TextField()
    )  # Flaw A3:2017-Sensitive Data Exposure (Storing unencrypted secret_key)
    created_at = models.DateTimeField(default=timezone.now)
    is_encrypted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # Fix A3:2017-Sensitive Data Exposure (Encrypt the secret_key before saving)
    def save(self, *args, **kwargs):
        if not self.is_encrypted and settings.ENABLE_ENCRYPTION:
            try:
                self.secret_key = cipher_suite.encrypt(
                    self.secret_key.encode()
                ).decode()
                self.is_encrypted = True
            except Exception as e:
                logger.error(f"Encryption failed: {e}")
                raise
        super().save(*args, **kwargs)

    # Fix A3:2017-Sensitive Data Exposure (Encrypt the secret_key before saving)
    def get_decrypted_key(self):
        return cipher_suite.decrypt(self.secret_key.encode()).decode()
