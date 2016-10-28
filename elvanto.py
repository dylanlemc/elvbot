import os

import asyncio
import ujson
from aiohttp import client

ELVANTO_KEY = os.environ.get('ELVANTO_KEY')

async def fetch_matched_people(payload: dict) -> list:
    headers = {'content-type': 'application/json'}
    response = await client.post(
        'https://api.elvanto.com/v1/people/search.json',
        data=ujson.dumps(payload),
        auth=(ELVANTO_KEY, '_'),
        headers=headers
    )
    data = ujson.loads(await response.read())
    if data['status'] == 'ok':
        people = data['people']['person']
        if people is None:
            people = []
    else:
        people = []

    return people

async def search_people(search_text: str) -> list:
    search_terms = search_text.split()
    payloads = []
    for search_term in search_terms:
        payloads.append({'search': {'firstname': search_term}})
        payloads.append({'search': {'lastname': search_term}})
        payloads.append({'search': {'preferred_name': search_term}})

    people = []
    coroutines = [fetch_matched_people(payload) for payload in payloads]
    results = await asyncio.gather(*coroutines)
    for data in results:
        if data is not None:
            people += data

    return people
