from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserListListView.as_view(), name='lists-view'),
    path('<str:name>/<str:username>', views.UserListDetailView.as_view(), name='lists-detail'),
    path('add/', views.UserListCreateView.as_view(), name='lists-add'),
    path('<int:pk>/', views.UserListUpdateView.as_view(), name='lists-update'),
    path('<int:pk>/delete/', views.UserListDeleteView.as_view(), name='lists-delete'),
]
