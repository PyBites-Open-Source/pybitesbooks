from django.conf.urls import url

from myreadinglist import views as main_views
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^get_books/', main_views.get_books, name='get_books'),
    url(r'^user/(?P<username>.*)$', views.user_books, name='user_books'),
]
