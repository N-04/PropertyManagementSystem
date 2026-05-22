from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models.menu import Menu
from apps.users.serializers.menu_serializer import MenuSerializer
from apps.users.serializers.user_serializer import UserInfoSerializer
from apps.users.serializers.user_serializer import UserSerializer
from common.views.base_view import BaseView
from common.response.response import (
    success_response,
    error_response
)

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(
            data = request.data
        )
        if serializer.is_valid():
            user_obj = serializer.save()

            return success_response(
                data = UserSerializer(user_obj).data,
                msg = '创建成功'
            )
        return error_response(
            msg = '参数错误',
            errors = serializer.errors
        )

class UserInfoView(BaseView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserInfoSerializer(request.user)

        return Response({
            'code': 200,
            'msg': 'success',
            'data': serializer.data
        })

class UserMenusView(BaseView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        menus = Menu.objects.filter(
            role__user = request.user,
            parent = None
        ).distinct().order_by('sort')

        serializer = MenuSerializer(
            menus,
            many = True
        )

        return success_response(
            data = serializer.data
        )