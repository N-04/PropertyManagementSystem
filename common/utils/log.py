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
