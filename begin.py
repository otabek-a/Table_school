from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query
from data_students import *
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
def start(update,context):
    full_name = update.message.from_user.full_name
    user_nick = update.message.from_user.username
    relpy_key=[['📚 Students 🏫','👨‍🏫 Teachers 🎓']]
    key=ReplyKeyboardMarkup(relpy_key)
    if user_nick:
       update.message.reply_text(f'👋 Hello dear {user_nick} 💫, please choose one option ⬇️', reply_markup=key)
    if not user_nick:
        update.message.reply_text(f'👋 Hello dear {full_name} 💫, please choose one option ⬇️', reply_markup=key)
  