import hangups
import json
import plugins
import requests


_conf = dict()


def _initialise(bot):

    pr_repos = bot.get_config_option('pr_repos')

    if pr_repos:
        plugins.register_user_command(['prs'])
        _conf['pr_repos'] = pr_repos
    else:
        print('PRS: config.pr_repos required')


def prs(bot, event, *args):

    segments = list()

    segments.append(
        hangups.ChatMessageSegment('Open pull requests:', is_bold=True)
    )

    segments.append(
        hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
    )

    if args:
        repos = list(args)
    else:
        repos = _conf['pr_repos']

    for repo in repos:

        segments.append(
            hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
        )

        segments.append(
            hangups.ChatMessageSegment(
                '{repo}:'.format(repo=repo),
                is_bold=True
            )
        )

        segments.append(
            hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
        )

        results = requests.get(
            'https://api.github.com/repos/{repo}/pulls'.format(repo=repo),
            headers={'User-Agent': 'icbot v360.N0.SC0P3'}
        )

        if results.status_code == 200:

            prs = json.loads(results.text)

            if not prs:

                segments.append(
                    hangups.ChatMessageSegment(
                        '\n',
                        hangups.SegmentType.LINE_BREAK
                    )
                )

                segments.append(
                    hangups.ChatMessageSegment('No open pull requests')
                )

            else:

                for pr in prs:

                    segments.append(
                        hangups.ChatMessageSegment(
                            '\n',
                            hangups.SegmentType.LINE_BREAK
                        )
                    )

                    segments.append(
                        hangups.ChatMessageSegment('[{pr_number}] '.format(
                            pr_number=pr['number']
                        ))
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

                    segments.append(
                        hangups.ChatMessageSegment(
                            '\n',
                            hangups.SegmentType.LINE_BREAK
                        )
                    )

        else:

            segments.append(
                hangups.ChatMessageSegment(
                    '\n',
                    hangups.SegmentType.LINE_BREAK
                )
            )

            segments.append(
                hangups.ChatMessageSegment(
                    'Server returned HTTP status code: {status_code}'.format(
                        status_code=results.status_code
                    )
                )
            )

        segments.append(
            hangups.ChatMessageSegment('\n', hangups.SegmentType.LINE_BREAK)
        )

    bot.send_message_segments(event.conv, segments)
