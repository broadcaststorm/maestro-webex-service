# Maestro Bot UI

## Usage Information

This UI is a Webex Bot that needs to be added to a Webex space/room via
its email address (listed below).

### Commands for the bot

All commands should be prefixed with an '@' mention to "Lab Maestro" -
which will get substituted to **Lab** in the client to show it is
actually a mention. This is normal.

- **@Lab project list [name]**: produces a list of available projects
in the lab.  If [name] is optionally provided, the command will give
details about the specified project.

- **@Lab scenario list [name]**: produces a list of available scenarios
in the lab.  If [name] is optionally provided, the command will give
details about the specified scenario.


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
- SECRETS_DIR: Location of the access token text file to populated the env var
- WEBEX_TEAMS_ROOM_TITLE: Title of the Webex Messaging room for the lab management
- FLASK_ENV: development, production, etc.
- FLASK_APP: application for the web server environment (webex)

## Caveats

This bot is currently being written for a focused, single purpose back end
service. Only a single instance dedicated to a single space is being
supported at this time.

## Roadmap

- Black formatter
- Precommit hooks for flake8 and black
