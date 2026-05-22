from django.urls import path

from apps.repairs.views import RepairCreateView, RepairStatusView

from apps.repairs.views import (
    RepairCreateView,
    RepairListView
)

urlpatterns = [

    path(
        'create/',
        RepairCreateView.as_view()
    ),
    path(
        'list/',
        RepairListView.as_view()
    ),
    path(
        'status/<int:pk>/',
        RepairStatusView.as_view()
    ),

]