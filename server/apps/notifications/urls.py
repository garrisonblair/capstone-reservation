from django.urls import path

from apps.notifications.views.notification import NotificationList, NotificationCreate, NotificationDelete

urlpatterns = [
    path(r'notifications', NotificationList.as_view()),
    path(r'notify', NotificationCreate.as_view()),
    path(r'notifications/<int:pk>/delete', NotificationDelete.as_view())
]
