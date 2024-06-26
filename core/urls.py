from django.urls import path

from .views import home, message_board, subscribe, newsletter, newsletter_subscribe

urlpatterns = [
    path('', home, name='home'),
    path('message-board/', message_board, name='message_board'),
    path('subscribe/', subscribe, name='subscribe'),
    path('newsletter/', newsletter, name='newsletter'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
]
