#Library import
from telegram import Update, InlineKeyboardButton as button, InlineKeyboardMarkup as markup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import nest_asyncio
from uuid import uuid4

#Config import
try:
    from config.keychain import TOKEN
except ImportError:
    import os
    TOKEN = os.environ['TOKEN']
from about.tags import tags_metadata, contact_info
from config.db import conn

#Model import
from models.token import Token

#Setup
nest_asyncio.apply()
app = ApplicationBuilder().token(TOKEN).build()

#Bot commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            button("Option 1", callback_data="1"),
            button("Option 2", callback_data="2"),
        ],
        [button("Option 3", callback_data="3")],
    ]

    reply_markup = markup(keyboard)
    await update.message.reply_text(
        text = f"""Hello @{update.effective_user.username}! My name is Notigram, and I'll send you a  notification every time you ask me to 😋 
        \nPress Get Token to get started!""",
        reply_markup=reply_markup)

async def gen_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res_token = conn.cluster0.users.find_one({"user":str(update.effective_user.id)})
    if(res_token != None):
        await update.message.reply_text(f'Your token is: <code>{res_token["token"]}</code>',parse_mode='HTML')
        return

    new_token = dict(Token(
        user= str(update.effective_user.id),
        token = str(uuid4())
    ));

    conn.cluster0.users.insert_one(new_token)
    await update.message.reply_text(f'Great {update.effective_user.username}! your CLI token is: \n<code>{new_token["token"]}</code>',parse_mode="HTML")
    return

async def new_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res_token = conn.cluster0.users.find_one_and_delete({"user":str(update.effective_user.id)})
    new_token = dict(Token(
        user= str(update.effective_user.id),
        token = str(uuid4())
    ));

    conn.cluster0.users.insert_one(new_token)
    await update.message.reply_text(f"Your new token is: \n<code>{new_token['token']}</code> \n\nDon't lose it again ^^'",parse_mode='HTML')
    return

async def revoken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn.cluster0.users.find_one_and_delete({"user":str(update.effective_user.id)})
    await update.message.reply_text(f"It's done! You don't have a token anymore. \nPress /token if you ever want a new token again!")
    return

#Bot handlers
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("token", gen_token))
app.add_handler(CommandHandler("new_token", new_token))
app.add_handler(CommandHandler("revoke",revoken))

#start
app.run_polling()