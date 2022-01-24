#!/usr/bin/bash

# At this point, I like obscurity but uncomment this should we go primetime
# export HEROKU_APP_NAME=lab-maestro

heroku login
# Logging in... done
# Logged in as millerte@broadcaststorm.dev

if -z "${HEROKU_APP_NAME}"; then
    heroku create
    # Creating app... done, ⬢ safe-tundra-80304
    # https://safe-tundra-80304.herokuapp.com/ | https://git.heroku.com/safe-tundra-80304.git

    export HEROKU_APP_NAME=$(heroku info -s | grep web_url | cut -d= -f2)
    echo "Dynamically detect app name as ${HEROKU_APP_NAME}"
else
    heroku create ${HEROKU_APP_NAME}
fi

heroku labs:enable runtime-dyno-metadata -a ${HEROKU_APP_NAME}
heroku addons:create heroku-redis:hobby-dev
