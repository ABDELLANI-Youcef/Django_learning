from django.urls import path
from . import dashboards

urlpatterns = [
  path('stats/<user_id>', dashboards.DashboardStatsView.as_view()),
  path('post-list/<user_id>', dashboards.DashboardPostListsView.as_view()),
  path('comment-list', dashboards.DashboardCommentListView.as_view()),
  path('noti-list/<user_id>/',dashboards.DashboardNotificationsListView.as_view()),
  path('noti-mark-seen/', dashboards.DashboardMarkNotiSeenAPIView.as_view()),
  path('reply-comment', dashboards.DashboardReplyCommentAPIView.as_view()),
  path('post-create', dashboards.DashboardPostCreateAPIView.as_view())
]