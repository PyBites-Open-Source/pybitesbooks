from decouple import config
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import To, From, Mail

FROM_EMAIL = config('FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')
ME = 'me'
ALL = 'all'
PYBITES = 'PyBites'

sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))


def send_email(to_email, subject, body, from_email=FROM_EMAIL, html=True):
    from_email = From(email=from_email, name=PYBITES)

    to_email = ADMIN_EMAIL if to_email == ME else to_email
    to_email = To(to_email)

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

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body if not html else None,
        html_content=body if html else None
    )

    response = sg.send(message)

    if str(response.status_code)[0] != '2':
        # TODO logging
        print('ERROR sending message, status_code {}'.format(
            response.status_code)
        )

    return response


if __name__ == '__main__':
    send_email('test-email@gmail.com', 'my subject', 'my message')
