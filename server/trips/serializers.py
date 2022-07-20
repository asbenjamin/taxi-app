from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # new

from .models import Trip


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        #new user signs up with new password i.e if the keys are not existent, new ones will be added with values
        """I think this "if" will return items except with tuple keys"""
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        #set new key password = data from password 1 in the signup process, and create new user with the data
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name',
        )
        read_only_fields = ('id',)


class LogInSerializer(TokenObtainPairSerializer):  # new
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)         #get token from user data
        user_data = UserSerializer(user).data   #serialize user data
        for key, value in user_data.items():
            if key != 'id':                     #avoid overriding the id (userclaim-settings.py)
                token[key] = value              #set the each key in token = a value in user_data.items()
        return token


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated',)
