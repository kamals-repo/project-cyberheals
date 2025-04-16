from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Role
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from users.validators import validate_password, validate_username

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validate_email])
    username = serializers.CharField(required=True, max_length=50, validators=[validate_username])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data.get('is_staff', False),
            password=validated_data['password']
        ) 
        user.save()
        return user
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    

class RoleAssignSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    role = serializers.ChoiceField(choices=Role.ROLE_CHOICES)

    class Meta:
        model = Role
        fields = ['user_id', 'role']

    def create(self, validated_data):
        
        role_obj, created = Role.objects.update_or_create(
            user=validated_data['user'],
            defaults={'role': validated_data['role']}
        )
        return role_obj