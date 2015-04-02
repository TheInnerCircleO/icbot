def slap(bot, event, *args):

    if not args:

        bot.send_message(event.conv, 'Who should I slap?')

    message = '/me slaps {} around a bit with a large black cock'.format(args[0])

    bot.send_message(event.conv, message)
