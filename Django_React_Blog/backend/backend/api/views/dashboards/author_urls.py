from django.urls import path
from . import dashboards_view

urlpatterns = [
  path('stats/<user_id>', dashboards_view.DashboardStatsView.as_view()),
  path('post-list/<user_id>', dashboards_view.DashboardPostListsView.as_view()),
  path('comment-list', dashboards_view.DashboardCommentListView.as_view()),
  path('noti-list/<user_id>/',dashboards_view.DashboardNotificationsListView.as_view()),
  path('noti-mark-seen/', dashboards_view.DashboardMarkNotiSeenAPIView.as_view()),
  path('reply-comment', dashboards_view.DashboardReplyCommentAPIView.as_view()),
  path('post-create', dashboards_view.DashboardPostCreateAPIView.as_view()),
  path('post/edit/<post_id>', dashboards_view.DashboardPostEditAPIView.as_view())
]