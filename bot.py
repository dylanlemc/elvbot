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

    results = []
    for ID, person in people.items():

        url = 'https://{0}/admin/people/person/?id={1}'.format(
            ELVANTO_DOMAIN,
            ID
        )
        image = person['picture']
        title = '{firstname} {lastname}'.format(person)
        fields = []
        if person('phone'):
            fields.append({
                'title': 'Phone Number',
                'value': person['phone']
            })
        if person('email'):
            fields.append({
                'title': 'Email Address',
                'value': person['email']
            })
        if person('mobile'):
            fields.append({
                'title': 'Mobile Number',
                'value': person['mobile']
            })
        result = {
            'title': title,
            'title_link': url,
            'thumb_url': image
        }
        if fields:
            result['fields'] = fields
        else:
            result['text'] = 'No contact details found for {firstname} {lastname}'.format(person)
        results.append(result)



    response = {
        'text': intro_text,
        'attachments' : results
    }
    await slack.reply(post_data['response_url'], response)


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
