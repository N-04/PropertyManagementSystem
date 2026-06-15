# 文件说明：封装接口列表分页返回格式。

# 导入 DRF 分页类
from rest_framework.pagination import PageNumberPagination

# 导入 Response
from rest_framework.response import Response


# 自定义分页类
class CustomPageNumberPagination(PageNumberPagination):

    # 默认每页数量
    page_size = 10

    # 前端可自定义 page_size
    page_size_query_param = "page_size"

    # 最大每页数量
    max_page_size = 100

    # 页码参数名
    page_query_param = "page"

    # 自定义分页返回格式
    def get_paginated_response(self, data):

        return Response(
            {
                "code": 200,
                "msg": "success",
                "data": data,
                "total": self.page.paginator.count,
                "page": self.page.number,
                "page_size": self.page.paginator.per_page,
            }
        )
