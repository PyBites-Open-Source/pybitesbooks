# PyBites Reading List Django App

Our simple reading app that gets you to read more. As Peter Drucker said: _What gets measured gets managed_ and we wholeheartedly agree!

## Setup

1. Create a [virtual env](https://pybit.es/the-beauty-of-virtualenv.html) and activate it (`source venv/bin/activate`)
2. Install the dependencies: `pip install -r requirements.txt`
3. Create a database, e.g. `myreadinglist` and define the full DB URL for the next step, e.g. `DATABASE_URL=postgres://postgres:password@0.0.0.0:5435/myreadinglist`.
4. Set this env variable together with `SECRET_KEY` in a file called `.env` in the root of the project: `cp .env-template .env && vi .env`. That's the bare minium. If you want to have email working create a [Sendgrid](https://sendgrid.com/) account obtaining an API key. The other variables have sensible defaults.
5. Sync the DB: `python manage.py migrate`.
6. And finally run the app server: `python manage.py runserver`.

## Contributions

... are more than welcome, just [open an issue](https://github.com/pybites/pbreadinglist/issues) and/or [PR new features](https://github.com/pybites/pbreadinglist/pulls). 

Not sure where we can take this, happy to [discuss on Slack](https://codechalleng.es/settings/). 

Remember _leaders are readers_, enjoy the process, enjoy your reading!
