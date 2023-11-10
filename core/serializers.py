from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def valdate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists

        if email_exists:
            raise ValidationError("Email already used.")
        return 