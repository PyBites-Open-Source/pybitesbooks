from django.urls import path

from goal import views as goal_views

app_name = "goal"
urlpatterns = [
    path("", goal_views.set_goal, name="set_goal"),
]
