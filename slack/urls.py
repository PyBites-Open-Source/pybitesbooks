from django.conf.urls import url

from . import views

app_name = 'slack'
urlpatterns = [
    url(r'^$', views.get_book, name='get_book'),
]
