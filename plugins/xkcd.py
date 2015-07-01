import json
import requests

from random import randint
from re import match


def _get_comic(num=False):

    url = 'https://xkcd.com/info.0.json'

    if num:
        url = 'https://xkcd.com/{num}/info.0.json'.format(num=num)

    results = requests.get(url, headers={'User-Agent': 'icbot v360.N0.SC0P3'})

    if results.status_code != 200:

        raise ValueError(
            'Server returned HTTP status code: {status_code}'.format(
                status_code=results.status_code
            )
        )

    xkcd_obj = json.loads(results.text)

    return xkcd_obj


def xkcd(bot, event, *args):
    """/bot xkcd [comic_number | random]
    Fetch the specified XCKD comic by the comic number or get a random comic.
    Ommitting an argument returns the latest comic."""

    xkcd_obj = _get_comic()

    if args:

        if args[0] == 'random':

            xkcd_obj = _get_comic(randint(1, xkcd_obj['num']))

        elif match('^\d*$', args[0]):

            if int(args[0]) <= xkcd_obj['num'] and int(args[0]) >= 1:

                xkcd_obj = _get_comic(args[0])

            else:

                bot.send_message(event.conv, 'ERROR: Argument out of range')
                return

        else:

            bot.send_message(event.conv, 'ERROR: Invalid argument')
            return

    bot.send_message_parsed(
        event.conv,
        '{title}: https://xkcd.com/{num}'.format(
            title=xkcd_obj['safe_title'],
            num=xkcd_obj['num']
        )
    )
