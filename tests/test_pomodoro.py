from collections import Counter

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import pytest

from pomodoro.models import Pomodoro


@pytest.fixture
def pomo_user(db):
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def pomodoros(pomo_user, db):
    pomodoros = []
    for i in range(5):
        pomodoro = Pomodoro.objects.create(
            user=pomo_user, end=timezone.now(), minutes=25
        )
        pomodoros.append(pomodoro)
    return pomodoros


@pytest.fixture
def pomodoros_multi_week(pomo_user, db):
    pomodoros = []
    for week in range(1, 5):  # Creating Pomodoro objects for 4 weeks
        for _ in range(5):
            end_time = timezone.now() - timezone.timedelta(weeks=week)
            pomodoro = Pomodoro.objects.create(user=pomo_user, end=end_time, minutes=25)
            pomodoros.append(pomodoro)
    return pomodoros


def test_track_pomodoro(db, client, pomo_user, pomodoros):
    client.login(username="testuser", password="12345")

    response = client.post(reverse("pomodoro:track_pomodoro"), {"add": "True"})

    assert response.status_code == 200

    # check that a new pomodoro was created
    assert Pomodoro.objects.filter(user=pomo_user).count() == 6

    # check correct data is passed to the template
    pomodori = Pomodoro.objects.filter(user=pomo_user)
    week_stats = Counter(pomo.week for pomo in pomodori)
    assert response.context["week_stats"] == sorted(week_stats.items(), reverse=True)


def test_track_pomodoro_template_output(db, client, pomo_user, pomodoros_multi_week):
    client.login(username="testuser", password="12345")

    # 4 weeks in fixture, this post creates 5th week (see below in emoji counts)
    response = client.post(reverse("pomodoro:track_pomodoro"), {"add": "True"})

    assert response.status_code == 200

    # check that a new pomodoro was created
    expected_pomodori_count = 21
    assert Pomodoro.objects.filter(user=pomo_user).count() == expected_pomodori_count

    # check correct data is passed to the template
    pomodori = Pomodoro.objects.filter(user=pomo_user)
    week_stats = Counter(pomo.week for pomo in pomodori)
    assert response.context["week_stats"] == sorted(week_stats.items(), reverse=True)

    # check the content of the response
    pomo_goal = 12
    for week, count in week_stats.items():
        if count >= pomo_goal:
            assert f"{week} | 😄" in response.content.decode()
        else:
            assert f"{week} | 😭" in response.content.decode()

    # count the number of each emoji in the response
    # not exactly checking rows, but ok for now
    assert response.content.decode().count("🍅") == expected_pomodori_count
    expected_toread_count = (5 * pomo_goal) - expected_pomodori_count
    assert response.content.decode().count("📖") == expected_toread_count
