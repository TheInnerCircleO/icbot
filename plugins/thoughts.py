import hangups
import json
import re
import requests

from random import randint
from urllib import parse


def thoughts(bot, event, *args):
    """/bot thoughts [subject]"""

    query_string = parse.quote_plus(' '.join(args))

    results = requests.get(
        'http://www.reddit.com/search.json?q={}'.format(query_string),
        headers={'User-Agent': 'icbot v360.N0.SC0P3'}
    )

    if results.status_code != 200:

        bot.send_message(
            event.conv,
            'Hmmmmmm: {}'.format(results.status_code)
        )

        return

    results_obj = json.loads(results.text)

    total_results = len(results_obj['data']['children']) - 1

    if total_results == 0:

        bot.send_message(event.conv, 'Hmmm.')
        return

    rand_index = randint(0, min([total_results, 5]))

    topic = results_obj['data']['children'][rand_index]

    rerep = re.compile(re.escape('reddit'), re.IGNORECASE)

    title = rerep.sub(
        'The Inner Circle',
        topic['data']['title']
    )

    link = 'https://www.reddit.com{}'.format(topic['data']['permalink'])

    segments = [
        hangups.ChatMessageSegment(
            title,
            hangups.SegmentType.LINK,
            link_target=link
        )
    ]

    bot.send_message_segments(event.conv, segments)
