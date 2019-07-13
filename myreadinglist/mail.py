from decouple import config
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

FROM_EMAIL = config('FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ME = 'me'
ALL = 'all'

sg = sendgrid.SendGridAPIClient(apikey=config('SENDGRID_API_KEY'))


def send_email(to_email, subject, body, from_email=FROM_EMAIL, html=False):
    # newlines get wrapped in email, use html
    body = body.replace('\n', '<br>')

    # if local no emails
    if settings.LOCAL:
        print('local env - no email, only print send_email args:')
        print('to_email: {}'.format(to_email))
        print('subject: {}'.format(subject))
        print('body: {}'.format(body))
        print('from_email: {}'.format(from_email))
        print('html: {}'.format(html))
        print()
        return

    from_email = Email(from_email)

    to_email = ADMIN_EMAIL if to_email == ME else to_email
    to_email = Email(to_email)

    type_ = html and "text/html" or "text/plain"

    content = Content(type_, body)

    mail = Mail(from_email, subject, to_email, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    if str(response.status_code)[0] != '2':
        # TODO logging
        print('ERROR sending message, status_code {}'.format(
            response.status_code)
        )

    return response
