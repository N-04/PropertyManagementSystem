# 文件说明：封装接口列表分页返回格式。

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    """统一列表分页格式，兼容前端表格组件读取 count/results。"""

    # 默认每页 10 条，允许前端通过 page_size 控制但限制最大值。
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """将 DRF 默认分页信息包装成项目统一响应结构。"""

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
