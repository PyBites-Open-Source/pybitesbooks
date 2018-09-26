from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from . import views
from books import views as book_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^slack/', include('slack.urls', namespace='slack')),
    url(r'^books/', include('books.urls', namespace='books')),
    url(r'^users/(?P<username>.*)$', book_views.user_page, name='user_page'),
    url(r'^widget/(?P<username>.*)$', book_views.user_page_widget, name='user_page_widget'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'hey-bob/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
