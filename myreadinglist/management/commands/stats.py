from datetime import date
from decouple import config, Csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from myreadinglist.mail import send_email
from books.models import UserBook
from goal.models import Goal

PYBITES_EMAIL_GROUP = config('PYBITES_EMAIL_GROUP', cast=Csv())
FRIDAY = 4
ONE_WEEK_AGO = timezone.now() - timezone.timedelta(days=7)
COMPLETED = 'c'
SUBJECT = 'Weekly PyBites Books stats'
MSG = """
Usage stats:
- {num_total_users} total users ({num_new_users} new users joined last week).
- {num_books_clicked} books were clicked.
- {num_books_completed} books were completed (= {num_books_completed_pages} pages read).

New user profiles:
{new_user_profiles}

What books were completed last week?
{books_completed}

Most ambitious readers:
{goals}
"""
PROFILE_PAGE = settings.DOMAIN + "/users/{username}"


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

        all_users = User.objects.all()
        new_users = all_users.filter(
            date_joined__gte=ONE_WEEK_AGO)
        num_new_users = new_users.count()

        num_books_clicked = UserBook.objects.filter(
            inserted__gte=ONE_WEEK_AGO
        ).count()

        books_read_last_week = UserBook.objects.select_related(
            'book', 'user'
        ).filter(
            Q(completed__gte=ONE_WEEK_AGO) & Q(status=COMPLETED)
        ).order_by('user__username')

        num_books_completed = books_read_last_week.count()
        num_books_completed_pages = sum(
            int(ub.book.pages) for ub in books_read_last_week
        )
        new_user_profiles = '<br>'.join(
            PROFILE_PAGE.format(username=uu.username)
            for uu in new_users
        )

        books_completed = '<br>'.join(
            f'{ub.user.username}: {ub.book.title} > {ub.book.url}'
            for ub in books_read_last_week
        )

        goals = Goal.objects.all()
        goals_out = '<br>'.join([f'{go.user.username} => {go.number_books}'
                                 for go in goals])

        msg = MSG.format(num_total_users=all_users.count(),
                         num_new_users=num_new_users,
                         new_user_profiles=new_user_profiles,
                         num_books_clicked=num_books_clicked,
                         num_books_completed=num_books_completed,
                         num_books_completed_pages=num_books_completed_pages,
                         books_completed=books_completed,
                         goals=goals_out)

        for to_email in PYBITES_EMAIL_GROUP:
            send_email(to_email, SUBJECT, msg)
