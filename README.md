# PyBites Books

> What gets measured gets managed. - Peter Drucker

Our simple yet effective reading tracking app: [PyBites Books](https://pybitesbooks.com)

(Warning: it can be addictive and will cause you to read more!)

## Setup

1. Create a [virtual env](https://pybit.es/the-beauty-of-virtualenv.html) and activate it (`source venv/bin/activate`)
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a database, e.g. `pybites_books` and define the full DB URL for the next step, e.g. `DATABASE_URL=postgres://postgres:password@0.0.0.0:5432/pybites_books`.
4. Set this env variable together with `SECRET_KEY` in a file called `.env` in the root of the project: `cp .env-template .env && vi .env`. That's the bare minium. If you want to have email working create a [Sendgrid](https://sendgrid.com/) account obtaining an API key. Same for Slack integration, this requires a `SLACK_VERIFICATION_TOKEN`. The other variables have sensible defaults.
5. Sync the DB: `python manage.py migrate`.
6. And finally run the app server: `python manage.py runserver`.

## Local Via docker-compose

You can use docker / docker compose to run both the postgresql database as well as the app itself. This makes local testing a lot easier, and allows you to worry less about environmental details.

To run, simply run the below command.  This should spin up the db, and then the application which you can reach at http://0.0.0.0:8000.

`docker-compose rm && docker-compose build && docker-compose up`

### DB Data
In order to prevent recreating the DB every time you run docker-compose, and in order to keep state from use to use, a volume is mounted, and tied to the local directory database-data.  This is ignored in the .gitignore so that you don't accidentally upload data to github.

### .env-compose
This has environment variables set so that you can get up and running easily.  Tweak these as needed to add things like Slack and SendGrid integration.

## Contributions

... are more than welcome, just [open an issue](https://github.com/pybites/pbreadinglist/issues) and/or [PR new features](https://github.com/pybites/pbreadinglist/pulls).

Love books, join [our Slack #books channel](https://pybit.es/pages/community.html).

Remember _leaders are readers_, read every day!
