from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'message': 'user with username already exists'})
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'message': 'user with email already exists'})
        elif attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'message': 'Password fields do not match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True,
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
