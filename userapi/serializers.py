# serializers.py
from .models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    gender = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=10)
    date_of_birth = serializers.DateField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password',
            'first_name', 'last_name',
            'gender', 'phone_number', 'date_of_birth'
        ]

    def validate_email(self, value):
        """
        Check if the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # Token.objects.create(user=user)

        # Create the associated UserProfile
        UserProfile.objects.create(
            user=user,
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # Add other fields as necessary
        fields = ['gender', 'phone_number', 'date_of_birth']


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'userprofile']
