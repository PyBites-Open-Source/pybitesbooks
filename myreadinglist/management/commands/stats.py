from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from myreadinglist.mail import send_email
from books.models import UserBook
from goal.models import Goal

FRIDAY = 4
SUBJECT = 'weekly pbreadinglist stats'
MSG = """
Number of users: {users}
Number of books added last week: {books_added}
Reading goals: {goals}
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

        one_week_ago = date.today() - timedelta(days=7)

        books_added = UserBook.objects.filter(
            inserted__gte=one_week_ago
        ).count()

        goals = Goal.objects.all()
        goals_out = ', '.join([f'{go.user.username} => {go.number_books}'
                               for go in goals])

        msg = MSG.format(users=num_users,
                         books_added=books_added,
                         goals=goals_out)

        send_email('me', SUBJECT, msg)
