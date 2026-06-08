from django.urls import path

from apps.logs.views.operation_log_view import (
    OperationLogListView,
)
from apps.logs.views.operation_log_export_view import (
    OperationLogExportView,
)

urlpatterns = [
    path(
        "list/",
        OperationLogListView.as_view(),
    ),
    path(
        "export/",
        OperationLogExportView.as_view(),
    ),
]
