# PyBites Reading List

> What gets measured gets managed. - Peter Drucker 

Our simple yet effective reading app. (Warning: it can be addictive and will cause you to read more!) 

## Setup

1. Create a [virtual env](https://pybit.es/the-beauty-of-virtualenv.html) and activate it (`source venv/bin/activate`)
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a database, e.g. `myreadinglist` and define the full DB URL for the next step, e.g. `DATABASE_URL=postgres://postgres:password@0.0.0.0:5432/myreadinglist`.
4. Set this env variable together with `SECRET_KEY` in a file called `.env` in the root of the project: `cp .env-template .env && vi .env`. That's the bare minium. If you want to have email working create a [Sendgrid](https://sendgrid.com/) account obtaining an API key. Same for Slack integration, this requires a `SLACK_VERIFICATION_TOKEN`. The other variables have sensible defaults.
5. Sync the DB: `python manage.py migrate`.
6. And finally run the app server: `python manage.py runserver`.

## Contributions

... are more than welcome, just [open an issue](https://github.com/pybites/pbreadinglist/issues) and/or [PR new features](https://github.com/pybites/pbreadinglist/pulls). 

Love books, join [our Slack #books channel](https://pybit.es/pages/community.html). 

Remember _leaders are readers_, read every day!
