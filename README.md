# elvbot

A simple slack slash command to fetch contact details from Elvanto.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Getting Started

Prerequisites:

 * Elvanto account
 * Slack team

## Deploy to Heroku

This app will happily run on Heroku's free tier for most users.
The free tier sleeps the app after half an hour of inactivity and requires
that the app must be asleep for at least 6 hours a day. 
The app will take slightly longer to respond if it must be woken up, but
subsequent requests should be nice and snappy.

  1. Get your Elvanto [API Key](https://www.elvanto.com/api/getting-started/#api_key).
  2. Click the Deploy to Heroku Button above.
  3. Create a new Slack [slash command](https://api.slack.com/slash-commands) for your team. You can name it anything you like, `elvbot` works nicely.
  4. Add the url of your herokuapp to your slash command.
  5. Add the slash command token to your Heroku app.
  6. Go test it is all working.

## Running locally

    git clone git@github.com:monty5811/elvbot.git && cd elvbot
    pyvenv-3.5 venv
    . venv/bin/activate
    pip install -r requirements.txt
    # export ELVANTO_KEY=???
    # export ELVANTO_DOMAIN=???
    # export SLACK_USERS_WHITELIST=???
    # export SLACK_TOKEN=???
    gunicorn -k aiohttp.worker.GunicornWebWorker -w 2 -t 60 bot:app
