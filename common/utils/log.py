# 文件说明：封装 common/utils/log.py 中跨接口复用的工具函数。

from apps.logs.models.operation_log import OperationLog


def save_log(
    username,
    module,
    action,
):
    OperationLog.objects.create(
        username=username,
        module=module,
        action=action,
    )
