from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup
from tinydb import TinyDB, Query

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

      
def students(update,context):
    table=sqlite3.connect('students.db')
    otabek=table.cursor()
    relpy_key=[['➕ Add Student 📝','✏️ find students 🛠'],
               ['🗑 Clear List ❌','📋 Show All Students 👥'],
               ['🔙 Back ⬅️']]
    key=ReplyKeyboardMarkup(relpy_key)
    update.message.reply_text('📌 What would you like to do with student data? ⬇️', reply_markup=key)
def find (update,context):
     update.message.reply_text('📌 please  send any information of student after 🔍')
def find_students(update,context):
    table=sqlite3.connect('students.db')
    otabek=table.cursor()
    text=update.message.text
    text=text.replace('🔍','').replace(' ','')
    otabek.execute("SELECT * FROM students WHERE first_name = ? or last_name=?", (text,text))
    data = otabek.fetchall()
    if not data:
        update.message.reply_text(f'sorry i could not find {text}')
        return
    user='📋 **All Students List:**\n\n'
    for idx, i in enumerate(data, start=1):
        user += (
            f"📌 **Student №{idx}**\n"
            f"👤 First Name: {i[0]}\n"
            f"💻 Last Name: {i[1]}\n"
            f"📍 Location: {i[2]}\n"
            f"📞 Phone Number: {i[3]}\n"
            f"———————————————\n"
        )
    update.message.reply_text(user)










def add_students(update,context):
    
    update.message.reply_text('📩 Please send me student data in this format:\n\n'
                              '📝 first_name / last_name / location / phone_number 📞')

def add(update,context):
    matn=update.message.text
    text=update.message.text.split('/')
    if len(text) != 4:
        update.message.reply_text("⚠️ Error: Please send data in the correct format:\n\n"
                                  "📝 first_name / last_name / location / phone_number 📞")
        return
    table=sqlite3.connect('students.db')
    otabek=table.cursor()
    phone=str(text[3].strip())
    otabek.execute("SELECT * FROM students WHERE phone_number = ?", (phone,))
    result = otabek.fetchone()
    if result:
        update.message.reply_text(f'⚠️ This student {matn} already exists in the database! ❌')
        return 
    otabek.execute("INSERT INTO students (first_name, last_name, location, phone_number) VALUES (?, ?, ?, ?)", 
                   (text[0].strip().lower(), text[1].strip().lower(), text[2].strip().lower(), text[3].strip().lower()))
    update.message.reply_text("✅ Student added successfully! 🎉")
    table.commit()
    table.close()

def show_students(update,context):
    table=sqlite3.connect('students.db')
    otabek=table.cursor()
    otabek.execute("Select * from students")
    data=otabek.fetchall()
    user='📋 **All Students List:**\n\n'
    index=1
    if not data:
        update.message.reply_text('🚫 Sorry, your student list is empty! ❌')
        return
    for idx, i in enumerate(data, start=1):
        user += (
            f"📌 **Student №{idx}**\n"
            f"👤 First Name: {i[0]}\n"
            f"💻 Last Name: {i[1]}\n"
            f"📍 Location: {i[2]}\n"
            f"📞 Phone Number: {i[3]}\n"
            f"———————————————\n"
        )
    update.message.reply_text(user)

def clear_data(update,context):
     table=sqlite3.connect('students.db')
     otabek=table.cursor()
     otabek.execute('DELETE FROM students')
     table.commit()
     update.message.reply_text('🗑 You have successfully cleared the student list! ✅')
