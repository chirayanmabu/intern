from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs={
            'password': {
                "write_only": True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def valdate(self, attrs):
    #     email_exists = User.objects.filter(email=attrs['email']).exists

    #     if email_exists:
    #         raise ValidationError("Email already used.")
    #     return 