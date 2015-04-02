import hangups
import json
import re
import requests

from random import randint


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


def get_random_topic(seed):

    # Safe it
    re.sub(r'\W+', '', seed)

    url = 'http://www.reddit.com/search.json?q=%s' % seed

    # try:

    obj_results = get_json(url)

    total_results = len(obj_results['data']['children']) - 1
    rand_index = randint(0, min([total_results, 5]))

    topic_obj = obj_results['data']['children'][rand_index]

    return topic_obj

    # except:

    #     return []


def thoughts(bot, event, *args):

    try:

        seed = ' '.join(args)
        topic = get_random_topic(seed)

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

    except:

        bot.send_message(event.conv, 'Hmmm.')
