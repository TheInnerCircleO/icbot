import json
import requests

from random import randint
from re import match


def get_json(url):
    """
    TODO: Make this act sane when bad status_code or an Exception is thrown
    Grabs json from a URL and returns a python dict
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; \
               rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}

    json_result = requests.get(url, headers=headers)
    if json_result.status_code == 200:
        try:
            obj_result = json.loads(json_result.text)
            return obj_result
        except Exception as e:
            return e
    else:
        return json_result.status_code


def xkcd(bot, event, *args):

    xkcd_obj = get_json('http://xkcd.com/info.0.json')

    if args:

        if args[0] == 'random':

            xkcd_obj = get_json(
                'http://xkcd.com/{}/info.0.json'.format(
                    randint(1, xkcd_obj['num'])
                )
            )

        elif match('^\d*$', args[0]):

            if int(args[0]) <= xkcd_obj['num'] and int(args[0]) >= 1:

                xkcd_obj = get_json(
                    'http://xkcd.com/{}/info.0.json'.format(args[0])
                )

            else:

                bot.send_message(event.conv, 'ERROR: Argument out of range')
                return

        else:

            bot.send_message(event.conv, 'ERROR: Invalid argument')
            return

    bot.send_message_parsed(
        event.conv,
        '{}: http://xkcd.com/{}'.format(
            xkcd_obj['safe_title'],
            xkcd_obj['num']
        )
    )
