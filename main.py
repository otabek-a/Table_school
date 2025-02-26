from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
from data_students import *
from begin import start
from config import TOKEN
import sqlite3
table=sqlite3.connect('students.db')
otabek=table.cursor()
otabek.execute( """
Create Table if not exists students(
               first_name,
               last_name,
               location,
               phone_number)


    """ )
table.commit()

def check(update,context):
    text=update.message.text.strip().lower()
    if '/' in text :
        add(update, context)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text('🔙 Back ⬅️'),start))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text('📚 Students 🏫'),students))
dispatcher.add_handler(MessageHandler(Filters.text('📋 Show All Students 👥'),show_students))
dispatcher.add_handler(MessageHandler(Filters.text('➕ Add Student 📝'),add_students))
dispatcher.add_handler(MessageHandler(Filters.text('🗑 Clear List ❌'),clear_data))
dispatcher.add_handler(MessageHandler(Filters.text,check))
updater.start_polling()
updater.idle()
