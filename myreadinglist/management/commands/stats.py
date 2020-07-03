from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Q

from myreadinglist.mail import send_email
from books.models import UserBook
from goal.models import Goal

FRIDAY = 4
ONE_WEEK_AGO = date.today() - timedelta(days=7)
COMPLETED = 'c'
SUBJECT = 'weekly pbreadinglist stats'
MSG = """
Number of users: {num_users}
(new users last week: {new_users})

Number of books added last week: {books_clicked}

Books completed last week:
{books_completed}

Reading goals:
{goals}
"""


class Command(BaseCommand):
    help = 'email app stats'

    def add_arguments(self, parser):
        parser.add_argument(
            '--now',
            action='store_true',
            dest='now',
            help='flag to show stats now = bypass day of the week check',
        )

    def handle(self, *args, **options):
        run_now = options['now']

        # seems heroku does not support weekly cronjobs
        if not run_now and date.today().weekday() != FRIDAY:
            return

        num_users = User.objects.count()
        new_users = ', '.join(
            [u.username for u in
             User.objects.filter(date_joined__gte=ONE_WEEK_AGO)]
        )

        books_clicked = UserBook.objects.filter(
            inserted__gte=ONE_WEEK_AGO
        ).count()
        books_completed = '<br>'.join(
            [f'{ub.user.username}: {ub.book.title} ({ub.book.url})'
             for ub in
             UserBook.objects.select_related('book', 'user').filter(
                Q(inserted__gte=ONE_WEEK_AGO) |
                Q(updated__gte=ONE_WEEK_AGO),
                status=COMPLETED).order_by('user__username')]
        )

        goals = Goal.objects.all()
        goals_out = '<br>'.join([f'{go.user.username} => {go.number_books}'
                                 for go in goals])

        msg = MSG.format(num_users=num_users,
                         new_users=new_users,
                         books_clicked=books_clicked,
                         books_completed=books_completed,
                         goals=goals_out)

        for to_email in 'me julian@pybit.es bob@pybit.es'.split():
            send_email(to_email, SUBJECT, msg)
