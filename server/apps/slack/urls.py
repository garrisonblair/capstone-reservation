from django.urls import path
from apps.slack.views.slack import SlackView


urlpatterns = [
    path(r'slack', SlackView.as_view())
]
