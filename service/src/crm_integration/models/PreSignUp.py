import uuid
from django.db import models
from simple_history.models import HistoricalRecords

from authentication.models import Profile
from crm_integration.models import Crm_Integration

class PreSignUp(models.Model):
    history = HistoricalRecords()
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False) 

    email = models.EmailField(unique=True)
    
    origin = models.ForeignKey(Crm_Integration, verbose_name=("CRM de Origem"), on_delete=models.PROTECT)
    
    data = models.JSONField(verbose_name=("Dados Recebidos"), default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    
    created_by = models.ForeignKey(Profile, verbose_name=("Criado Por"), on_delete=models.SET_NULL, blank=True, null=True)
    
    is_finished = models.BooleanField(verbose_name=("Cadastro Concluído"), default=False)
    
    request_signup_id = models.UUIDField(verbose_name=("ID de Requisição de Cadastro"), blank=True, null=True)

    def __str__(self):
        return f"{self.email} ({self.origin.name})"

    class Meta:
        verbose_name = "Pré-Cadastro"
        verbose_name_plural = "Pré-Cadastros"
