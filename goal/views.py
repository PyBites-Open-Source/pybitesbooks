from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Goal


@login_required
def set_goal(request):
    post = request.POST
    user = request.user

    # take the current year, so switches to new challenge
    # when the new year starts
    goal, _ = Goal.objects.get_or_create(user=user,
                                         year=date.today().year)

    if 'updateGoal' in post:
        try:
            num_books = int(post.get('numBooks', 0))
        except ValueError:
            error = 'Please provide a numeric value'
            messages.error(request, error)
        else:
            old_number = goal.number_books

            goal.number_books = num_books
            goal.share = post.get('share', False)
            goal.save()

            action = 'added' if old_number == 0 else 'updated'
            msg = f'Successfully {action} goal for {goal.year}'
            messages.success(request, msg)

    return render(request, 'goal.html', {'goal': goal})
