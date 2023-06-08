from collections import Counter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from pomodoro.models import (Pomodoro,
                             DEFAULT_POMO_GOAL,
                             DEFAULT_POMO_MIN,
                             this_week)


@login_required
def track_pomodoro(request):
    post = request.POST
    user = request.user

    if post.get('add'):
        Pomodoro.objects.create(user=user, end=timezone.now())
        msg = 'Great job, another pomodoro done!'
        messages.success(request, msg)

    pomodori = Pomodoro.objects.filter(user=request.user)

    week_stats = Counter(pomo.week for pomo in pomodori)

    context = {
        'week_stats': sorted(week_stats.items(), reverse=True),
        'week_goal': DEFAULT_POMO_GOAL,
        'pomo_minutes': DEFAULT_POMO_MIN,
    }
    return render(request, 'pomodoro/pomodoro.html', context)
