#Library import
from telegram import Update, InlineKeyboardButton as button, InlineKeyboardMarkup as markup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler
import nest_asyncio
from uuid import uuid4

#Config import
try:
    from config.keychain import TOKEN
except ImportError:
    import os
    TOKEN = os.environ['TOKEN']
from about.tags import tags_metadata, contact_info, app_info
from config.db import conn

#Model import
from models.token import Token

#Setup
nest_asyncio.apply()
app = ApplicationBuilder().token(TOKEN).build()

HANDLER,GEN,NEW,REVOKE,ABOUT = range(5)
stdmarkup = markup([
    [
        button("Token",callback_data=str(GEN)),
        button("Generate New",callback_data=str(NEW))
    ],
    [
        button("Revoke Token",callback_data=str(REVOKE)),
        button("About",callback_data=str(ABOUT))
    ]
])

#Bot commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [
        [button("Get Token", callback_data=str(GEN))],
        [button("About",callback_data=str(ABOUT))]
        ]
    reply_markup = markup(keyboard)

    await update.message.reply_text(
        text = f"""Hello @{update.effective_user.username}! My name is Notigram, and I'll send you a  notification every time you ask me to 😋 
        \nPress <code>Get Token</code> to get started!""",
        parse_mode='HTML',
        reply_markup=reply_markup)
    return HANDLER

async def gen_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    res_token = conn.cluster0.users.find_one({"user":str(update.effective_user.id)})

    if(res_token != None):
        await query.edit_message_text(
            text=f'Your token is: <code>{res_token["token"]}</code>',
            parse_mode='HTML',
            reply_markup=stdmarkup 
        )
        return HANDLER

    new_token = dict(Token(
        user= str(update.effective_user.id),
        token = str(uuid4())
    ));

    conn.cluster0.users.insert_one(new_token)
    await query.edit_message_text(
        text=f'Great {update.effective_user.username}! your new CLI token is: \n<code>{new_token["token"]}</code>',
        parse_mode="HTML",
        reply_markup=stdmarkup
    )
    return HANDLER

async def new_token(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    res_token = conn.cluster0.users.find_one_and_delete({"user":str(update.effective_user.id)})
    new_token = dict(Token(
        user= str(update.effective_user.id),
        token = str(uuid4())
    ));

    conn.cluster0.users.insert_one(new_token)
    await query.edit_message_text(
        text=f"Your new token is: \n<code>{new_token['token']}</code> \n\nDon't lose it again ^^'",
        parse_mode='HTML',
        reply_markup=stdmarkup
    )
    return HANDLER

async def revoken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    conn.cluster0.users.find_one_and_delete({"user":str(update.effective_user.id)})
    await query.edit_message_text(
        text=f"It's done! You don't have a token anymore. \nPress <code>Token</code> or <code>Generate New</code> if you ever want a new token again!",
        parse_mode='HTML',
        reply_markup=stdmarkup)
    return HANDLER

async def hadouken(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=app_info['info'],
        parse_mode='HTML',
        reply_markup=stdmarkup)
    return HANDLER

#Bot handlers
conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HANDLER: [
                CallbackQueryHandler(gen_token, pattern="^" + str(GEN) + "$"),
                CallbackQueryHandler(new_token, pattern="^" + str(NEW) + "$"),
                CallbackQueryHandler(revoken, pattern="^" + str(REVOKE) + "$"),
                CallbackQueryHandler(hadouken, pattern="^" + str(ABOUT) + "$")
            ]
        },
        fallbacks=[CommandHandler("start", start)],
    )
app.add_handler(conv_handler)

#start
app.run_polling()