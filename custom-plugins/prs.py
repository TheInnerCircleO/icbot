import hangups
import json
import requests


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


def prs(bot, event, *args):

    prs = get_json(
        'https://api.github.com/repos/TheInnerCircleO/hangupsbot/pulls'
    )

    if not prs:
        bot.send_message(event.conv, 'No open pull requests')
        return

    segments = [
        hangups.ChatMessageSegment('Open pull requests:', is_bold=True)
    ]

    for pr in prs:
        segments.append(
            hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
        )

        segments.append(
            hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
        )

        segments.append(
            hangups.ChatMessageSegment('[{}] '.format(pr['number']))
        )

        segments.append(
            hangups.ChatMessageSegment(
                pr['title'],
                hangups.SegmentType.LINK,
                link_target=pr['html_url']
            )
        )

        segments.append(hangups.ChatMessageSegment(' by '))

        segments.append(
            hangups.ChatMessageSegment(
                pr['user']['login'],
                hangups.SegmentType.LINK,
                link_target=pr['user']['url']
            )
        )

    bot.send_message_parsed(event.conv, segments)
