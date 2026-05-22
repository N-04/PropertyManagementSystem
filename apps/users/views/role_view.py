from rest_framework.views import APIView
from apps.users.models.role import Role

from apps.users.serializers.role_serializer import RoleSerializer
from apps.users.serializers.role_serializer import RoleSerializer
from apps.users.services.role_service import RoleService

from common.response.response import (
    success_response,
    error_response
)

from common.pagination.base_pagination import BasePagination


class RoleCreateView(APIView):

    def post(self, request):

        serializer = RoleSerializer(
            data = request.data
        )

        if serializer.is_valid():

            role_obj = RoleService.create_role(
                serializer
            )

            return success_response(
                data = RoleSerializer(role_obj).data,
                msg = '创建成功'
            )

        return error_response(
            msg = '参数错误',
            errors = serializer.errors
        )


class RoleListView(APIView):

    def get(self, request):

        queryset = RoleService.get_role_list()

        paginator = BasePagination()

        page_queryset = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = RoleSerializer(
            page_queryset,
            many = True
        )

        return paginator.get_paginated_response({
            'code': 200,
            'msg': 'success',
            'data': serializer.data
        })


class RoleDetailView(APIView):

    def get(self, request, pk):

        role_obj = RoleService.get_role_by_id(pk)

        if not role_obj:

            return error_response(
                code = 404,
                msg='角色不存在'
            )

        return success_response(
            data=RoleSerializer(role_obj).data
        )

class RoleUpdateView(APIView):

    def put(self, request, pk):

        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:

            return error_response(
                msg='角色不存在'
            )

        serializer = RoleSerializer(
            role,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                data=serializer.data,
                msg='更新成功'
            )

        return error_response(
            msg='参数错误',
            errors=serializer.errors
        )