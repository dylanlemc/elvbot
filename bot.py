import asyncio
import elvanto
import slack
from aiohttp import client, web

async def send_reply(post_data):
    people = await elvanto.search_people(post_data['text'])
    intro_text = 'You searched Elvanto for "{0}"\nHere are your results:\n'.format(
        post_data['text']
    )

    results_text = ''
    for person in people:
        t = '\t*{0} {1}*\n\t\t{2}\n\t\tphone: {3}\n\t\tmobile: {4}\n'.format(
            person['firstname'],
            person['lastname'],
            person['email'],
            person['phone'],
            person['mobile'],
        )
        results_text += t

    resp_text = intro_text + results_text
    await slack.reply(post_data['response_url'], resp_text)


async def aio_search_people(request):
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
