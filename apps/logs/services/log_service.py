# 文件说明：封装 apps/logs/services/log_service.py 对应业务的可复用服务逻辑。

# 操作日志模型
from apps.logs.models import OperationLog


def save_operation_log(
    username,
    module,
    action,
):
    """
    保存操作日志

    username : 用户名
    module   : 模块名称
    action   : 操作内容
    """

    OperationLog.objects.create(
        username=username,
        module=module,
        action=action,
    )
