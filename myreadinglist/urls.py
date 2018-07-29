from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/get_books/', views.get_books, name='get_books'),
    url(r'^books/(?P<bookid>.*)$', views.book_page, name='book_page'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'hey-bob/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
