from rest_framework.views import APIView
from apps.users.models.menu import Menu
from apps.users.serializers.menu_serializer import MenuSerializer

from common.response.response import (
    success_response,
    error_response
)


class MenuCreateView(APIView):

    def post(self, request):

        serializer = MenuSerializer(
            data=request.data
        )

        if serializer.is_valid():

            menu_obj = serializer.save()

            return success_response(
                data=MenuSerializer(menu_obj).data,
                msg='创建成功'
            )

        return error_response(
            msg='参数错误',
            errors=serializer.errors
        )


class MenuListView(APIView):

    def get(self, request):

        queryset = Menu.objects.all().order_by('sort')

        serializer = MenuSerializer(
            queryset,
            many=True
        )

        return success_response(
            data=serializer.data
        )

class MenuTreeView(APIView):

    def get(self, request):

        queryset = Menu.objects.filter(
            parent__isnull = True
        ).order_by('sort')

        data = []

        for item in queryset:

            children = Menu.objects.filter(
                parent = item
            ).order_by('sort')

            data.append({
                'id': item.id,
                'title': item.title,
                'icon': item.icon,
                'path': item.path,
                'component': item.component,
                'children': MenuSerializer(
                    children,
                    many = True
                ).data
            })

        return success_response(
            data = data
        )