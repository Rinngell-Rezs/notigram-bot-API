#Library import
from telegram.ext import ApplicationBuilder
from fastapi import FastAPI

#Config import
import os
from about.tags import tags_metadata, contact_info
from config.db import conn

#models
from models.request import messageRequest

#Setup
TOKEN = os.environ['bot_TOKEN']
bot = ApplicationBuilder().token(TOKEN).build()
API = FastAPI(
    title="Notigram API",
    description="Esto se va a ver chulísimo en producción 7u7r",
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact=contact_info,
    debug=True
)

#API Routes
@API.post('/sendMessage')
async def sendMessage(req:messageRequest):
    user = conn.cluster0.users.find_one({'token':req.token});
    if(user == None):
        return {'error':'Invalid token.'}
    await bot.bot.send_message(user['user'],req.message,parse_mode='HTML')
    return {'response':'Success.'}

@API.get('/sendMessage')
async def sendMessage():
    return {'response':'Nice try,but try sending a POST request next time.'}

@API.get('/')
async def sendMessage():
    return {'response':'There\'s nothing in here. Try at /sendMessage .'}