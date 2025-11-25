from django.db import models
from simple_history.models import HistoricalRecords
from django.conf import settings
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

import uuid
import re


class Crm_Integration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False) 

    history = HistoricalRecords()

    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    url = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CRM Integration"
        verbose_name_plural = "CRM Integrations"
    
    def get_absolute_url(self, email):
        return self.url.replace("{email}", email)
