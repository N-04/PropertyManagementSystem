from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers.auth_serializer import LoginSerializer


class LoginView(APIView):

    authentication_classes = []

    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            return Response(
                {
                    'code': 400,
                    'msg': '用户名或密码错误'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        })