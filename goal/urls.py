from django.conf.urls import url

from goal import views as goal_views

app_name = 'goal'
urlpatterns = [
    url(r'^$', goal_views.set_goal, name='set_goal'),
]
