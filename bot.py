# pip install python-telegram-bot
import telegram.bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackQueryHandler)
from telegram.ext.dispatcher import run_async
import logging
from functools import wraps
import random
import time
from params import bottoken, port, admin, chat
import json
from datetime import datetime

# pip install pyopenssl
from requests import get
ip = get('https://api.ipify.org').text
try:
    certfile = open("cert.pem")
    keyfile = open("private.key")
    certfile.close()
    keyfile.close()
except IOError:
    from OpenSSL import crypto
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().CN = ip
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')
    with open("cert.pem", "wt") as certfile:
        certfile.write(crypto.dump_certificate(
            crypto.FILETYPE_PEM, cert).decode('ascii'))
    with open("private.key", "wt") as keyfile:
        keyfile.write(crypto.dump_privatekey(
            crypto.FILETYPE_PEM, key).decode('ascii'))

logging.basicConfig(filename='debug.log', filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

TARGET, CONTENT = range(2)


def collector():
    json.dumps('', indent=4, sort_keys=True)


def adminonly(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id == admin:
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text(
                '`Admin Only`', parse_mode=telegram.ParseMode.MARKDOWN)
    return wrapped


@adminonly
def start(update, context):
    msg = '''
*Prayer Partner CountMeIn*

*I'm a guy: assign randomly* (0)

*I'm a girl: assign randomly* (0)

*I'm a guy: assign same gender* (0)

*I'm a girl: assign same gender* (0)

    '''
    keyboard = [
        [InlineKeyboardButton(
            "I'm a guy: assign randomly", callback_data='Guy')],
        [InlineKeyboardButton(
            "I'm a girl: assign randomly", callback_data='Girl')],
        [InlineKeyboardButton(
            "I'm a guy: assign same gender", callback_data='OnlyGuy')],
        [InlineKeyboardButton(
            "I'm a girl: assign same gender", callback_data='OnlyGirl')],
        [InlineKeyboardButton("Remove my name", callback_data='Remove')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=chat, text=msg, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)


def loader():
    global x
    try:
        with open('x.json') as xfile:
            x = {}
            x = json.load(xfile)
    except:
        with open('x.json', 'w+') as xfile:
            x = {}
    global users
    try:
        with open('users.json') as userfile:
            users = {}
            users = json.load(userfile)
    except:
        with open('users.json', 'w+') as userfile:
            users = {}


def callbackquery(update, context):
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    query = update.callback_query
    data = query.data
    user_id = str(query.from_user.id)
    first_name = query.from_user.first_name
    last_name = query.from_user.last_name
    full_name = (str(first_name or '') + ' ' + str(last_name or '')).strip()
    global users
    users[user_id] = full_name
    with open('users.json', 'w') as userfile:
        json.dump(users, userfile)
    global x
    x.setdefault('Guy', [])
    x.setdefault('Girl', [])
    x.setdefault('OnlyGuy', [])
    x.setdefault('OnlyGirl', [])
    if data == 'Guy':
        if user_id not in x['Guy']:
            x['Guy'].append(user_id)
        if user_id in x['Girl']:
            x['Girl'].remove(user_id)
        if user_id in x['OnlyGuy']:
            x['OnlyGuy'].remove(user_id)
        if user_id in x['OnlyGirl']:
            x['OnlyGirl'].remove(user_id)
    if data == 'Girl':
        if user_id not in x['Girl']:
            x['Girl'].append(user_id)
        if user_id in x['Guy']:
            x['Guy'].remove(user_id)
        if user_id in x['OnlyGuy']:
            x['OnlyGuy'].remove(user_id)
        if user_id in x['OnlyGirl']:
            x['OnlyGirl'].remove(user_id)
    if data == 'OnlyGuy':
        if user_id not in x['OnlyGuy']:
            x['OnlyGuy'].append(user_id)
        if user_id in x['Guy']:
            x['Guy'].remove(user_id)
        if user_id in x['Girl']:
            x['Girl'].remove(user_id)
        if user_id in x['OnlyGirl']:
            x['OnlyGirl'].remove(user_id)
    if data == 'OnlyGirl':
        if user_id not in x['OnlyGirl']:
            x['OnlyGirl'].append(user_id)
        if user_id in x['Guy']:
            x['Guy'].remove(user_id)
        if user_id in x['Girl']:
            x['Girl'].remove(user_id)
        if user_id in x['OnlyGuy']:
            x['OnlyGuy'].remove(user_id)
    if data == 'Remove':
        if user_id in x['Guy']:
            x['Guy'].remove(user_id)
        if user_id in x['Girl']:
            x['Girl'].remove(user_id)
        if user_id in x['OnlyGuy']:
            x['OnlyGuy'].remove(user_id)
        if user_id in x['OnlyGirl']:
            x['OnlyGirl'].remove(user_id)
    with open('x.json', 'w') as xfile:
        json.dump(x, xfile)
    guy = ''
    for item in x['Guy']:
        guy += users[item] + '\n'
    girl = ''
    for item in x['Girl']:
        girl += users[item] + '\n'
    onlyguy = ''
    for item in x['OnlyGuy']:
        onlyguy += users[item] + '\n'
    onlygirl = ''
    for item in x['OnlyGirl']:
        onlygirl += users[item] + '\n'
    if (len(x['Guy']) + len(x['Girl']) + len(x['OnlyGuy']) + len(x['OnlyGirl'])) % 2 != 0:
        odd = '_1 on waitlist due to odd number_\n'
    else:
        odd = '\n'
    msg = '''
*Prayer Partner CountMeIn*
{}
*I'm a guy: assign randomly* ({})
{}
*I'm a girl: assign randomly* ({})
{}
*I'm a guy: assign same gender* ({})
{}
*I'm a girl: assign same gender* ({})
{}
_Last updated: {}_
    '''.format(odd, len(x['Guy']), guy, len(x['Girl']), girl, len(x['OnlyGuy']), onlyguy, len(x['OnlyGirl']), onlygirl, current_time)
    keyboard = [
        [InlineKeyboardButton(
            "I'm a guy: assign randomly", callback_data='Guy')],
        [InlineKeyboardButton(
            "I'm a girl: assign randomly", callback_data='Girl')],
        [InlineKeyboardButton(
            "I'm a guy: assign same gender", callback_data='OnlyGuy')],
        [InlineKeyboardButton(
            "I'm a girl: assign same gender", callback_data='OnlyGirl')],
        [InlineKeyboardButton("Remove my name", callback_data='Remove')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=msg,
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )
    context.bot.answer_callback_query(query.id)


def main():
    updater = Updater(token=bottoken, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callbackquery))

    loader()

    #updater.start_polling()
    updater.start_webhook(listen='0.0.0.0',
                          port=port,
                          url_path=bottoken,
                          key='private.key',
                          cert='cert.pem',
                          webhook_url='https://{}:{}/{}'.format(ip, port, bottoken))

    print("Bot is running. Press Ctrl+C to stop.")
    print("Please wait for confirmation before closing.")
    updater.idle()
    print("Bot stopped successfully.")


if __name__ == '__main__':
    main()
