from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import generics, serializers, response, status, views
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, RegistrationSerializer


# Create your views here.

class UserRegister(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class UserDataAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLoginView(views.APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]

    @staticmethod
    def post(request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        try:
            user_object = User.objects.get(username=username)
            if not user_object.is_active:
                raise Exception({
                    'success': False,
                    'message': "Account inactive"
                })
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'success': False,
                'message': "Invalid credentials"
            })

        except Exception as err:
            raise serializers.ValidationError({
                'success': False,
                'message': err
            })
        user = authenticate(username=user_object.username, password=password)
        if not user:
            raise serializers.ValidationError({
                'success': False,
                'message': "Invalid credentials"
            })

        user.last_login = timezone.now()
        try:
            token = Token.objects.get(user=user).key
        except Exception as err:
            print(err)
            token = Token.objects.create(user=user).key
        user.save()

        return response.Response(
            {
                "success": True,
                "message": "success",
                "data": {"token": str(token),
                         "email": user.email,
                         "username": user.username,
                         },
                "errors": "null",
            },
            status=status.HTTP_200_OK,
        )
