#!/usr/bin/bash

if -z "${SECRETS_DIR}"; then
    echo "Set a SECRETS_DIR location for token.txt"
    exit 1
fi

export WEBEX_TEAMS_ACCESS_TOKEN=$(cat ${SECRETS_DIR}/token.txt)
export WEBEX_TEAMS_ROOM_TITLE='GVE RTP Lab - Scenario Management'

if -z "${WEBEX_TEAMS_ACCESS_TOKEN}"; then
    echo "Application requires a Webex Bot Token to be defined."
    exit 1
fi

heroku config:set WEBEX_TEAMS_ACCESS_TOKEN=${WEBEX_TEAMS_ACCESS_TOKEN}
# Setting WEBEX_TEAMS_ACCESS_TOKEN and restarting ... done, v5

heroku config:set WEBEX_TEAMS_ROOM_TITLE="${WEBEX_TEAMS_ROOT_TITLE}
# Setting WEBEX_TEAMS_ROOM_TITLE and restarting ... done, v6
