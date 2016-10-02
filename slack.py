import os

try:
    import ujson
except ImportError:
    import json as ujson

from aiohttp import client


def check_user_has_access(username: str) -> bool:
    SLACK_USERS_WHITELIST = os.environ.get('SLACK_USERS_WHITELIST')
    if SLACK_USERS_WHITELIST is None:
        return True

    SLACK_USERS_WHITELIST = SLACK_USERS_WHITELIST.split(',')
    SLACK_USERS_WHITELIST = [s.strip() for s in SLACK_USERS_WHITELIST]

    if username in SLACK_USERS_WHITELIST:
        return True
    else:
        print('Request from unauthorised user: {0}'.format(username))
        return False


def check_token(token: str) -> bool:
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    if SLACK_TOKEN is None:
        return True
    if token == SLACK_TOKEN:
        return True
    else:
        print('Invalid access token used: {0}'.format(token))
        return False


async def reply(url: str, body: dict):
    headers = {'content-type': 'application/json'}
    response = await client.post(
        url,
        data=ujson.dumps(body),
        headers=headers
    )
    print('Replied with {0}'.format(body))
