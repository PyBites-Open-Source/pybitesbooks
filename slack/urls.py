from django.urls import path

from . import views

app_name = 'slack'
urlpatterns = [
    path('', views.get_book, name='get_book'),
]
