from decouple import config
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import To, From, Mail

FROM_EMAIL = config('FROM_EMAIL')
PYBITES = 'PyBites'

sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))


def send_email(to_email, subject, body, from_email=FROM_EMAIL, html=True):
    from_email = From(email=from_email, name=PYBITES)
    to_email = To(to_email)

    # if local no emails
    if settings.LOCAL:
        body = body.replace('<br>', '\n')
        print('local env - no email, only print send_email args:')
        print(f'to_email: {to_email.email}')
        print(f'subject: {subject}')
        print(f'body: {body}')
        print(f'from_email: {from_email.email}')
        print(f'html: {html}')
        print()
        return

    # newlines get wrapped in email, use html
    body = body.replace('\n', '<br>')
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
        print(f'ERROR sending message, status_code {response.status_code}')

    return response


if __name__ == '__main__':
    send_email('test-email@gmail.com', 'my subject', 'my message')
