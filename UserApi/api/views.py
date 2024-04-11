from datetime import datetime, timedelta
import uuid


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

import jwt
from django.conf import settings
from .serializers import UserSerializer
from .models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Создаем нового пользователя, если данные валидны
            user = User.objects.create_user(username=request.data['email'], email=request.data['email'], password=request.data['password'])
            # Возвращаем успешный ответ с данными пользователя
            return Response({'id': user.id, 'email': user.email}, status=status.HTTP_201_CREATED)
        else:
            # Если данные невалидны, возвращаем ошибку с деталями о невалидных данных
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # authenticate использует username => приравниваем к username
        user = authenticate(username=email, password=password)
        if user is None:
            return Response({'error': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token_payload = {
            'user_id': user.id,
            'exp': datetime.now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY)
        }
        # PyJwt encoding
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = str(uuid.uuid4())
        return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', "Bearer ").split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Response({'token': decoded_token})