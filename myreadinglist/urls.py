from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views
from books import views as book_views

urlpatterns = [
    path('', views.index, name='index'),
    path('query_books/', views.query_books, name='query_books'),
    path('api/', include('api.urls', namespace='api')),
    path('slack/', include('slack.urls', namespace='slack')),
    path('books/', include('books.urls', namespace='books')),
    path('users/<str:username>', book_views.user_page, name='user_page'),
    path('widget/<str:username>', book_views.user_page_widget, name='user_page_widget'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('5hours/', include('pomodoro.urls')),
    path('goal/', include('goal.urls')),
    path('super-reader/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
