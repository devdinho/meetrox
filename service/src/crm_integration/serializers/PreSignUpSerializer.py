from rest_framework import serializers
from django.shortcuts import get_object_or_404

from crm_integration.models import PreSignUp, Crm_Integration
from authentication.models import Profile
import requests


class PreSignUpSerializer(serializers.ModelSerializer):
    """Serializer para o modelo de Pré-Cadastro.

    ### Utilizado para converter objetos de Pré-Cadastro em JSON e vice-versa.

    Campos:
    - id: Identificador único do pré-cadastro.
    - email: Endereço de e-mail do pré-cadastro.
    - origin: CRM de origem do pré-cadastro.
    - data: Dados recebidos no pré-cadastro.
    - created_at: Data e hora de criação do pré-cadastro.
    - created_by: Usuário que criou o pré-cadastro.
    """

    class Meta:
        model = PreSignUp
        fields = (
            "email",
            "origin",
        )
        read_only_fields = ("created_at", "created_by")
        
    def create(self, validated_data):
        email = validated_data.get("email", None).lower()
        crm = validated_data.get("origin", None)

        if PreSignUp.objects.filter(email=email, origin=crm).exists():
            raise serializers.ValidationError("E-mail já cadastrado.")

        crm_object = get_object_or_404(Crm_Integration, id=crm.id)
        
        if not crm_object or not crm_object.is_active:
            raise serializers.ValidationError("CRM de origem inativo.")

        new_pre_signup = PreSignUp(
            email=validated_data.get("email", None).lower(),
            origin=validated_data.get("origin", None),
            created_by=self.context["request"].user,
        )

        data_response = requests.get(
            crm_object.get_absolute_url(email=new_pre_signup.email),
            headers={"Authorization": f"Bearer {crm_object.api_key}"},
        )
        
        if data_response.status_code != 200:
            raise serializers.ValidationError("Erro ao conectar com o CRM de origem.")
        
        new_pre_signup.data = data_response.json()
        print(f"DATA RESPONSE: {new_pre_signup.data}")
        crm_properties = new_pre_signup.data.get("properties")
        
        if crm_properties:
            new_pre_profile = Profile.objects.create(
                email=crm_properties.get("email"),
                first_name=crm_properties.get("firstname"),
                last_name=crm_properties.get("lastname"),
                username=crm_properties.get("email"),
                is_active=False,
                password=self.make_random_password(),
            )
            new_pre_profile.save()
            
        
        try:
            new_pre_signup.save()
        except Exception as e:
            raise serializers.ValidationError(str(e.__cause__))

        return new_pre_signup
    
    def make_random_password(self, length=10, allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"):
        import random

        return "".join(random.choice(allowed_chars) for _ in range(length))