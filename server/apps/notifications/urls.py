from django.urls import path

from apps.notifications.views.notification import NotificationList, NotificationCreate

urlpatterns = [
    path(r'notifications', NotificationList.as_view()),
    path(r'notify', NotificationCreate.as_view())
]
