def slap(bot, event, *args):

    if not args:

        bot.send_message(event.conv, 'Who should I slap?')

    txt = '/me slaps {} around a bit with a large black cock'
    message = txt.format(args[0])

    bot.send_message(event.conv, message)
