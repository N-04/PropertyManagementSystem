# 文件说明：配置站内即时通讯接口路由。
from django.urls import path

from apps.chat.views import (
    ChatConversationCreateView,
    ChatConversationDetailView,
    ChatConversationListView,
    ChatConversationRatingView,
    ChatConversationStatusView,
    ChatMessageCreateView,
)

urlpatterns = [
    path("conversation/list/", ChatConversationListView.as_view()),
    path("conversation/create/", ChatConversationCreateView.as_view()),
    path("conversation/detail/<int:pk>/", ChatConversationDetailView.as_view()),
    path("conversation/status/<int:pk>/", ChatConversationStatusView.as_view()),
    path("conversation/rating/<int:pk>/", ChatConversationRatingView.as_view()),
    path("conversation/<int:pk>/message/create/", ChatMessageCreateView.as_view()),
]
