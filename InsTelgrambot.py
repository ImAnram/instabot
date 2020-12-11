import instabot
from telegram import ext
import telegram as tel

updater = ext.Updater('1213036895:AAGr_3QzZ8_UhSwpBB2dJUe454wV0dZvv0o')


def start(bot, update):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    text_start = f'سلام {first_name} \n \
        /login برای شروع کار با ربات باید با \n \
         شروع کنید وبعد از لاگین یوز نیم وپسورد \n \
         اینستاگرامتون رو وارد کنید مثال: \n \
            /login username password'
    bot.sendMessage(chat_id, text_start)


class InsTelgram:
    def __init__(self):
        self.username, self.password = '', ''
        self.like, self.follow = True, False
        self.comment, self.items = None, None
        self.num = 0
        self.mod, self.insta, self.data = '', None, ''

    def login(self, bot, update, args):
        chat_id = update.message.chat_id
        if len(args) == 2:
            self.username = args[0]
            self.password = args[1]
            self.job(bot, update)
        else:
            bot.sendMessage(chat_id, 'لطفا بعد از /login یوزر نیم و پسورد را بنویسید\
                                        مانند مثال:\n \
                                            /login username password')

    def job(self, bot, update):
        chat_id = update.message.chat_id
        if self.password:
            keyboard_j1 = [
                [
                    tel.InlineKeyboardButton('user👥', callback_data='user'),
                    tel.InlineKeyboardButton('hashtag#️⃣', callback_data='tag'),
                    tel.InlineKeyboardButton('search🔍', callback_data='search')
                ],
                [
                    tel.InlineKeyboardButton('comment💬', callback_data='comment'),
                    tel.InlineKeyboardButton('like👍', callback_data='like'),
                    tel.InlineKeyboardButton('follow👤', callback_data='follow')
                ],
                [
                    tel.InlineKeyboardButton('ok✅', callback_data='ok')
                ]
            ]
            if self.insta:
                self.insta.Quit()
                bot.sendMessage(chat_id, 'بات متوقف شد')
            text_job = f'اطلاعات را تکمیل کنید و درصورت اشتباه تصحیح کنید \n \
             و در آخر بر روی ok✅ کلیک کنید \n \n \
            👤 یوزرنیم : -->{self.username} \n \
            🔑 پسورو : -->{self.password} \n \
           🔎 مدل جستجو : --> {self.mod} \n \
           🔍 لیست جستجو : --> {self.items} \n \
            💬لیست کامنتا : --> {self.comment} \n \
            👍وضعیت لایک : --> {self.like} \n \
            👤وضعیت فالو : --> {self.follow} \n \
           🔢 تعداد پست ها : --> {self.num} \n'
            bot.sendMessage(chat_id, text_job,
                            reply_markup=tel.InlineKeyboardMarkup(keyboard_j1))
        else:
            bot.sendMessage(chat_id, 'لطفا اول لاگین را کامل کنید !')

    def message_filter(self, bot, update):
        tags = update.message.text
        tag_list = tags.split(',')
        if self.data == 'tag' or self.data == 'user':
            self.items = tag_list[:-1]
            self.num = int(tag_list[-1].strip())
        elif self.data == 'comment':
            self.comment = tag_list
        elif self.data == 'search':
            self.num = int(tags.strip())
        self.job(bot, update)

    def callback(self, bot, update):
        query = update.callback_query
        self.data = query.data
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        if self.data == 'tag' or self.data == 'user':
            self.mod = self.data
            textReply = 'خب هالا {0} مورد نضر را بفرستین و با , از هم جدا کنید \n \
                   و در اخر این که چند تا پست باشه رو بنویسید مثال\n \
                    {0},{0},200'.format(self.data)
            bot.sendMessage(chat_id=chat_id, text=textReply)
            tags_message = ext.MessageHandler(ext.Filters.text,
                                              telBot.message_filter)
            updater.dispatcher.add_handler(tags_message)

        elif self.data == 'search':
            self.mod = 'search'
            textReply = 'تعداد پست هایی که میخواهید کار انجام بدید را وارد کنید'
            bot.sendMessage(chat_id=chat_id, text=textReply)
            tags_message = ext.MessageHandler(ext.Filters.text,
                                              telBot.message_filter)
            updater.dispatcher.add_handler(tags_message)

        elif self.data == 'follow':
            self.follow = not self.follow
            bot.sendMessage(chat_id=chat_id, text=f'follow --> {self.follow}',
                            reply_to_message_id=message_id)

        elif self.data == 'like':
            self.like = not self.like
            bot.sendMessage(chat_id=chat_id, text=f'like --> {self.like}',
                            reply_to_message_id=message_id)

            self.job(bot, update)
        elif self.data == 'comment':
            textReply = 'خب هالا {0} مورد نضر را بفرستین و با , از هم جدا کنید \
                    {0},{0} :مثال'.format(self.data)
            bot.sendMessage(chat_id=chat_id, text=textReply)
            tags_mess = ext.MessageHandler(ext.Filters.text,
                                           telBot.message_filter)
            updater.dispatcher.add_handler(tags_mess)

        elif self.data == 'ok':
            bot.editMessageText(text='خب بات شروع به کار کرد',
                                chat_id=chat_id, message_id=message_id)
            self.insta = instabot.InstagramBot()
            self.insta.login(self.username, self.password)
            if self.mod == 'tag':
                self.insta.tag(self.items, self.num, self.like,
                               self.follow, self.comment)
            elif self.mod == 'user':
                self.insta.user(self.items, self.num, self.like, self.comment)
            elif self.mod == 'search':
                self.insta.search(self.num, self.like, self.follow, self.comment)

            self.insta.Quit()
            bot.sendMessage(text='پایان کار', chat_id=chat_id)


telBot = InsTelgram()

start_command = ext.CommandHandler('start', start)
updater.dispatcher.add_handler(start_command)

clear_command = ext.CommandHandler('clear', telBot)
updater.dispatcher.add_handler(clear_command)

login_command = ext.CommandHandler('login', telBot.login, pass_args=True)
updater.dispatcher.add_handler(login_command)

login_command = ext.CommandHandler('job', telBot.job)
updater.dispatcher.add_handler(login_command)

callback1_handler = ext.CallbackQueryHandler(telBot.callback)
updater.dispatcher.add_handler(callback1_handler)

updater.start_polling()
updater.idle()
