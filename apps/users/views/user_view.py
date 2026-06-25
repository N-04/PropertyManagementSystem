# 文件说明：处理 apps/users/views/user_view.py 对应接口请求，编排查询、创建、修改和删除等业务流程。

from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import Role
from apps.users.models.menu import Menu
from apps.users.models.user import User
from apps.users.serializers.login_serializer import LoginSerializer
from apps.users.serializers.user_serializer import (
    CurrentUserPasswordSerializer,
    CurrentUserProfileSerializer,
    UserAuditSerializer,
    UserInfoSerializer,
    UserSerializer,
)
from apps.users.utils.role_access import is_property_manager_user
from apps.users.utils.validators import mask_id_card, validate_phone_format
from apps.users.views.menu_view import _build_menu_tree_list, _get_user_menu_ids
from common.pagination.page_pagination import CustomPageNumberPagination
from common.response.response import ResponseError, ResponseSuccess
from common.views.base_view import BaseView


class UserCreateView(APIView):
    """
    用户创建接口

    请求方式：
        POST

    请求地址：
        /api/user/create/

    前端提交数据：

    {
        "username": "repair2",
        "password": "123456",
        "role_ids": [1, 2]
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权创建用户")

        # =====================================================
        # 1. 获取前端提交的数据
        # =====================================================

        # 获取用户名
        username = request.data.get("username")

        # 获取密码
        password = request.data.get("password")

        # 获取角色ID数组
        # 例如：
        # [1, 2]
        role_ids = request.data.get("role_ids", [])

        real_name = request.data.get("real_name")

        phone = request.data.get("phone")

        status = request.data.get("status", 1)

        # =====================================================
        # 2. 数据校验
        # =====================================================

        # 用户名不能为空
        if not username:

            return Response({"code": 400, "msg": "用户名不能为空"})

        # 密码不能为空
        if not password:

            return Response({"code": 400, "msg": "密码不能为空"})

        # =====================================================
        # 3. 判断用户名是否存在
        # =====================================================

        # exists():
        # 判断数据库是否存在数据
        if User.objects.filter(username=username).exists():

            return Response({"code": 400, "msg": "用户名已存在"})

        # =====================================================
        # 4. 创建用户
        # =====================================================

        """
        注意：

        这里只先创建用户名

        密码后面单独加密
        """

        user = User.objects.create_user(
            username=username,
            password=password,
            real_name=real_name,
            phone=phone,
            status=status,
        )

        # =====================================================
        # 6. 查询角色
        # =====================================================

        """
        role_ids:

            [1, 2]

        SQL效果：

            where id in (1, 2)
        """

        roles = Role.objects.filter(id__in=role_ids)

        # =====================================================
        # 7. 绑定角色
        # =====================================================

        """
        user.roles：

            多对多字段

        set():

            设置多对多关系
        """

        # 保存角色
        user.roles.set(roles)

        # 返回结果
        return Response({"code": 200, "msg": "创建成功"})


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权删除用户")

        try:

            user = User.objects.get(id=pk)

        except User.DoesNotExist:

            return Response({"code": 404, "msg": "用户不存在"})

        user.delete()

        return Response({"code": 200, "msg": "删除成功"})


# 用户详情接口
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # =====================================================
    # 获取用户详情
    # =====================================================
    def get(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权查看用户")

        # 根据ID查询用户
        user = get_object_or_404(User, id=pk)

        # 返回数据
        return Response(
            {
                "code": 200,
                "data": {
                    # 用户ID
                    "id": user.id,
                    # 用户名
                    "username": user.username,
                    # 真实姓名
                    "real_name": user.real_name,
                    # 手机号
                    "phone": user.phone,
                    "id_card_masked": mask_id_card(user.id_card),
                },
            }
        )

    # =====================================================
    # 修改用户
    # =====================================================
    def put(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权修改用户")

        """
        pk:

            用户ID

        request.data:

            前端提交的数据
        """

        # =====================================================
        # 1. 查询用户
        # =====================================================

        user = get_object_or_404(User, id=pk)

        update_fields = []

        if "username" in request.data:
            username = str(request.data.get("username") or "").strip()

            if not username:
                return ResponseError(msg="用户名不能为空")

            if User.objects.exclude(id=user.id).filter(username=username).exists():
                return ResponseError(msg="用户名已存在")

            user.username = username
            update_fields.append("username")

        if "real_name" in request.data:
            user.real_name = request.data.get("real_name") or ""
            update_fields.append("real_name")

        if "phone" in request.data:
            raw_phone = request.data.get("phone") or ""

            if raw_phone:
                try:
                    raw_phone = validate_phone_format(raw_phone)
                except Exception as exc:
                    detail = getattr(exc, "detail", None)
                    msg = str(detail[0]) if isinstance(detail, list) and detail else "手机号格式不正确"
                    return ResponseError(msg=msg)

            user.phone = raw_phone or None
            update_fields.append("phone")

        # =====================================================
        # 4. 保存
        # =====================================================

        if update_fields:
            user.save(update_fields=update_fields)

        # =====================================================
        # 5. 返回结果
        # =====================================================

        return Response({"code": 200, "msg": "修改成功"})


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return ResponseSuccess(data=serializer.data)

    def put(self, request):
        serializer = CurrentUserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return ResponseSuccess(data=UserInfoSerializer(user).data, msg="资料修改成功")


class CurrentUserPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = CurrentUserPasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["password"])
        request.user.save(update_fields=["password"])

        return ResponseSuccess(msg="密码修改成功，请重新登录")


class UserMenusView(BaseView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        menu_ids = _get_user_menu_ids(request.user)

        root_menus = Menu.objects.filter(
            parent__isnull=True,
            id__in=menu_ids,
            hidden=False,
        ).order_by("sort", "id")

        data = _build_menu_tree_list(root_menus, menu_ids)

        return ResponseSuccess(data=data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权查看用户列表")

        queryset = User.objects.all().order_by("-id")
        keyword = request.GET.get("keyword", "").strip()

        if keyword:
            # 用户列表搜索只匹配页面可见的用户名、姓名、手机号和角色名。
            queryset = queryset.filter(
                Q(username__icontains=keyword)
                | Q(real_name__icontains=keyword)
                | Q(phone__icontains=keyword)
                | Q(roles__name__icontains=keyword)
            ).distinct()

        # 实例化分页器
        paginator = CustomPageNumberPagination()

        # 分页
        page_queryset = paginator.paginate_queryset(queryset, request)

        # 序列化
        serializer = UserSerializer(page_queryset, many=True)

        # 返回分页数据
        return paginator.get_paginated_response(serializer.data)


class UserAuditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if not is_property_manager_user(request.user):
            return ResponseError(msg="无权审核用户")

        user = get_object_or_404(User, id=pk)
        serializer = UserAuditSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.validated_data["audit_status"] == "approved" and not user.roles.exists():
            owner_role = Role.objects.filter(code="owner").first()

            if owner_role:
                user.role = owner_role
                user.roles.set([owner_role])
                user.save(update_fields=["role"])

        return ResponseSuccess(data=UserSerializer(user).data, msg="审核完成")


# 用户登录接口
class LoginView(APIView):

    def post(self, request):

        # 获取前端数据
        serializer = LoginSerializer(data=request.data)

        # 验证数据
        serializer.is_valid(raise_exception=True)

        # 获取用户名密码
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        # Django 用户认证
        user = authenticate(username=username, password=password)

        # 用户不存在
        if not user:
            return ResponseError(msg="用户名或密码错误")

        # 生成 token
        refresh = RefreshToken.for_user(user)

        # 返回 token
        return ResponseSuccess(
            data={"token": str(refresh.access_token), "refresh": str(refresh)},
            msg="登录成功",
        )
