from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate,login
from django.db.models import Q


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password','is_admin']

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            password=validated_data['password'],
            is_admin=validated_data['is_admin']
        )
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(Q(username__iexact=username))
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Credentials')

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        return attrs

    def authenticate(self):
        username = self.data.get('username')
        password = self.data.get('password')
        user = User.objects.get(Q(username__iexact=username))
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        login(self.context.get('request'), user)
        return user
    

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username','email','phone')