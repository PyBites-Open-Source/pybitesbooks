from celery import shared_task

from books.goodreads import convert_goodreads_to_google_books


@shared_task
def convert_goodreads_to_google_books(csv_upload, request):
    return convert_goodreads_to_google_books(
        csv_upload, request, sleep_seconds=1)
