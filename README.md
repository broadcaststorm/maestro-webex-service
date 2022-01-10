# Maestro Bot UI

## Bot Information

- Name: Lab Maestro
- Email: lab-maestro@webex.bot
- Description: "Webex Bot to provide frontend into the Lab Maestro microservices application responsible for lab setup and orchestration."
- Token: defined in WEBEX_TEAMS_ACCESS_TOKEN environment variable

## Requirements

- Python 3.9+
- [Flake8 4.0.x](https://flake8.pycqa.org/en/latest/)
- [Flask 2.0.x](https://flask.palletsprojects.com/en/2.0.x/)
- [Gunicorn 20.1.x](https://docs.gunicorn.org/en/latest/index.html)
- [Webex Messaging SDK](https://webexteamssdk.readthedocs.io/en/latest/index.html)

- [Heroku CLI](https://devcenter.heroku.com/categories/command-line)

## Environment Variables

- WEBEX_TEAMS_ACCESS_TOKEN: API Access Token specific to Bot for Webex Messaging
- FLASK_ENV: development, production, etc.
- FLASK_APP: application for the web server environment (webex)

## Roadmap

- Black formatter
- Precommit hooks for flake8 and black