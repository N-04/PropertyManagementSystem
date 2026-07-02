# 文件说明：声明 Python 包，便于模块被项目导入。

from .notice_view import (
    NoticeCreateView,
    NoticeDeleteView,
    NoticeDetailView,
    NoticeListView,
    NoticeUpdateView,
)

__all__ = [
    "NoticeCreateView",
    "NoticeDeleteView",
    "NoticeDetailView",
    "NoticeListView",
    "NoticeUpdateView",
]
