from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer,LoginSerializer,UserDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": response.data,
            "token": token.key
        })
        
        
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.authenticate()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'key': token.key, 'detail': UserDetailSerializer(user).data}, status=status.HTTP_200_OK)
    
    
class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        data = {
            'pk': user.pk, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
            'last_name': user.last_name,

        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)