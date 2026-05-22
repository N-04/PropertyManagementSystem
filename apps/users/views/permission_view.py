from rest_framework.views import APIView

from apps.users.serializers.permission_serializer import PermissionSerializer
from apps.users.services.permission_service import PermissionService

from common.pagination.base_pagination import BasePagination
from common.response.response import error_response
from common.response.response import success_response


class PermissionListView(APIView):

    def get(self, request):

        queryset = PermissionService.get_permission_list(
            request.GET
        )

        paginator = BasePagination()

        page_queryset = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = PermissionSerializer(
            page_queryset,
            many=True
        )

        return paginator.get_paginated_response(
            success_response(
                data=serializer.data
            ).data
        )
class PermissionCreateView(APIView):

    def post(self, request):

        serializer = PermissionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            permission_obj = PermissionService.create_permission(
                serializer
            )

            return success_response(
                data=PermissionSerializer(permission_obj).data,
                msg='创建成功'
            )

        return error_response(
            msg='参数错误',
            errors=serializer.errors
        )
class PermissionDetailView(APIView):

    def get(self, request, pk):

        permission_obj = PermissionService.get_permission_by_id(
            pk
        )

        if not permission_obj:

            return error_response(
                msg='权限不存在',
                code=404
            )

        serializer = PermissionSerializer(
            permission_obj
        )

        return success_response(
            data=serializer.data
        )
class PermissionUpdateView(APIView):

    def put(self, request, pk):

        permission_obj = PermissionService.get_permission_by_id(
            pk
        )

        if not permission_obj:

            return error_response(
                msg='权限不存在',
                code=404
            )

        serializer = PermissionSerializer(
            permission_obj,
            data=request.data
        )

        if serializer.is_valid():

            permission_obj = PermissionService.update_permission(
                serializer
            )

            return success_response(
                data=PermissionSerializer(permission_obj).data,
                msg='更新成功'
            )

        return error_response(
            msg='参数错误',
            errors=serializer.errors
        )
class PermissionDeleteView(APIView):

    def delete(self, request, pk):

        permission_obj = PermissionService.get_permission_by_id(
            pk
        )

        if not permission_obj:

            return error_response(
                msg='权限不存在',
                code=404
            )

        PermissionService.delete_permission(
            permission_obj
        )

        return success_response(
            msg='删除成功'
        )