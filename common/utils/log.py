# 文件说明：封装 common/utils/log.py 中跨接口复用的工具函数。

from apps.logs.models.operation_log import OperationLog


def save_log(
    username,
    module,
    action,
):
    """写入操作日志，供后台审计列表统一展示。"""

    # 这里只负责最小日志字段，复杂审计内容由业务视图先组装好再传入。
    OperationLog.objects.create(
        username=username,
        module=module,
        action=action,
    )
