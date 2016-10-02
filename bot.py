import asyncio
import elvanto
import os
import slack
from aiohttp import web

async def send_reply(post_data: dict):
    people = await elvanto.search_people(post_data['text'])
    intro_text = 'You searched Elvanto for "{0}"\nHere are your results:\n'.format(
        post_data['text']
    )

    ELVANTO_DOMAIN = os.environ.get('ELVANTO_DOMAIN')

    results_text = ''
    for ID, person in people.items():
        if ELVANTO_DOMAIN:
            url = 'https://{0}/admin/people/person/?id={1}'.format(
                ELVANTO_DOMAIN,
                ID
            )
            person['ur'] = url
            t = '\t*<url|{firstname} {lastname}>*\n\t\t{email}\n\t\tphone: {phone}\n\t\tmobile: {mobile}\n'.format(person)
        results_text += t

    resp_text = intro_text + results_text
    await slack.reply(post_data['response_url'], resp_text)


async def aio_search_people(request) -> web.Response:
    await request.post()
    if not slack.check_token(request.POST['token']):
        return web.Response(
            body=b'Woops, invalid Slack token.',
            content_type='text/plain'
        )

    if not slack.check_user_has_access(request.POST['user_name']):
        return web.Response(
            body=b'Woops, you don\'t have access',
            content_type='text/plain'
        )

    asyncio.ensure_future(
        send_reply(
            request.POST,
        )
    )
    return web.Response(
        body=b'Searching...\n',
        content_type='text/plain'
    )

app = web.Application()
app.router.add_route('POST', '/', aio_search_people)
