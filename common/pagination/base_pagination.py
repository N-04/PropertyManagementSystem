# 文件说明：封装接口列表分页返回格式。

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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


# 手写 APIView 分页分块：给未使用 DRF 通用视图的列表接口复用。
def parse_positive_int(raw_value, default):
    """把分页参数安全转成正整数，非法值使用默认值。"""

    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return default

    return value if value > 0 else default


def paginate_queryset(queryset, request, default_page_size=10, max_page_size=100):
    """统一手写 APIView 的分页逻辑，避免异常参数 500 或一次性返回全量数据。"""

    page = parse_positive_int(request.GET.get("page"), 1)
    page_size = parse_positive_int(request.GET.get("page_size"), default_page_size)
    # 限制最大 page_size，避免调用方绕过分页一次性拉取大列表。
    page_size = min(page_size, max_page_size)
    paginator = Paginator(queryset, page_size)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        # 页码过大时落到最后一页，保持接口可用并避免 500。
        page = paginator.num_pages or 1
        page_obj = paginator.page(page)

    return page_obj.object_list, {
        "total": paginator.count,
        "count": paginator.count,
        "page": page,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
    }


def build_paginated_data(results, meta):
    """把序列化结果和分页元信息组合成前端统一可读结构。"""

    return {
        "results": results,
        **meta,
    }
