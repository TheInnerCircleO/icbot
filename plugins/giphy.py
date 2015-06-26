import aiohttp
import io
import json
import os
import requests

from random import choice
from urllib import parse


def giphy(bot, event, *args):
    """Reaction gifs deliverd to you in 30 minutes or less"""

    # if not args:
    #     bot.send_message(event.conv, 'What are you looking for?')
    #     return

    results = requests.get(
        '{search_url}?api_key={api_key}&q={query}'.format(
            search_url='https://api.giphy.com/v1/gifs/search',
            api_key='dc6zaTOxFJmzC',
            query=parse.quote_plus(' '.join(args))
        ),
        headers={'User-Agent': 'icbot v360.N0.SC0P3'}
    )

    if results.status_code != 200:

        bot.send_message(
            event.conv,
            'ERROR: {}'.format(results.status_code)
        )

        return

    results_obj = json.loads(results.text)['data']

    gif = choice(results_obj)

    image = gif['images']['downsized_large']['url']

    filename = os.path.basename(image)
    r = yield from aiohttp.request('get', image)
    raw = yield from r.read()
    image_data = io.BytesIO(raw)

    image_id = yield from bot._client.upload_image(
        image_data,
        filename=filename
    )

    bot.send_message_segments(event.conv.id_, None, image_id=image_id)
