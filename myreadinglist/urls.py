from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/get_books/', views.get_books, name='get_books'),
    url(r'hey-bob/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
