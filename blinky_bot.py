#!/usr/bin/ python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from PIL import Image
from ffmpy import FFmpeg
from filelock import Timeout, FileLock
import pickle
import os
import glob
file_path = "/home/pi/ws2812b/config/waiting_line"
lock_path = "/home/pi/ws2812b/config/waiting_line.lock"

lock = FileLock(lock_path, timeout=10)

gif_counter = 0

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def brightness(update, context):
    """Send a message when the command /brightness is issued."""
    option = glob.glob('/home/pi/ws2812b/config/BRIGHTNESS=*')
    print(context.args[0])
    os.rename(option[0], '/home/pi/ws2812b/config/BRIGHTNESS=' + context.args[0])


def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    update.message.reply_text("""Sorry this is not a gif or a picture and 
I have no clue how to write text to that display thing there.
I mean have you seen how that works? It's fucking nuts.
I don't even know how to make letters that small and 
I'm just an everyday bot. \n\n
Anyways, wanna give me a gif or a picture so I can resize it 
to 20x15 pixel and show you? :D""")

def gif_handler(update, context):
    print('Gif Handler')
    global gif_counter
    try:
        mp4 = context.bot.getFile(update.message.document.file_id)
        mp4.download('media.mp4')
        ff = FFmpeg(
                inputs={'media.mp4': '-y'}, #TODO REmove the -y ??/
                #outputs={'blinky.gif': '-s 20x15'})
                outputs={'/home/pi/ws2812b/gifs/' + str(gif_counter) + '.gif': '-s 20x15'})
        ff.run()
    except:
        print('FFmpeg Error!')
    try:
        with lock:
            with open(file_path, 'r') as f:
                line = f.read()
            with open(file_path, 'w') as f:
                f.write(line + str(gif_counter) + ',')
        gif_counter += 1
    except Timeout:
        print('Cant accuire lock!')


def image_handler(update, context):
    print('Image Handler')
    global gif_counter
    try:
        pic = context.bot.getFile(update.message.photo[-1].file_id)
        pic.download('photo.gif')
        ff = FFmpeg(
                inputs={'photo.gif': '-y'}, #TODO REmove the -y ??/
                outputs={'/home/pi/ws2812b/gifs/' + str(gif_counter) + '.gif': '-s 20x15'})
        ff.run()
    except:
        print('FFmpeg Error!')
    try:
        with lock:
            with open(file_path, 'r') as f:
                line = f.read()
            with open(file_path, 'w') as f:
                f.write(line + str(gif_counter) + ',')
        gif_counter += 1
    except Timeout:
        print('Cant accuire lock!')


def voice_handler(update, context):
    print('voice Handler')
    fid = update.message.voice.file_id
    data = context.bot.getFile(file_id=fid)
    print ("file_id: " + str(update.message.voice.file_id))
    data.download('voice.ogg')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def init_waiting_line():
    try:
        with lock:
            pfile = open(file_path, 'wb')
            waiting_line = []
            pickle.dump(waiting_line, pfile)
        gif_counter += 1
    except Timeout:
        print('Cant accuire lock!')



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    with open('/home/pi/ws2812b/telegram_token', 'r') as f:
        token = f.read()[:-1]
    logger.info(f'Token: {token}')
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("brightness", brightness))

    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_handler(MessageHandler(Filters.photo, image_handler))
    dp.add_handler(MessageHandler(Filters.document.mime_type("video/mp4"), gif_handler))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
