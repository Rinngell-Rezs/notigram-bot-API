#Library import
from telegram.ext import ApplicationBuilder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Config import
try:
    from config.keychain import TOKEN
except ImportError:
    import os
    TOKEN = os.environ['TOKEN']
from about.tags import tags_metadata, contact_info
from config.db import conn

#models
from models.request import messageRequest

#Setup
bot = ApplicationBuilder().token(TOKEN).build()
API = FastAPI(
    title="Notigram API",
    description="Esto se va a ver chulísimo en producción 7u7r",
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact=contact_info,
    debug=True
)

API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#API Routes
@API.get('/')
async def home():
    await bot.bot.send_message(184075777,"Ya haz dos apps en vez de una, boluda xD",parse_mode='HTML');
    return {'message':'Hello from the API'}

@API.post('/sendMessage')
async def sendMessage(req:messageRequest):
    user = conn.cluster0.users.find_one({'token':req.token});
    if(user == None):
        return {'error':'Invalid token.'}
    await bot.bot.send_message(user['user'],req.message,parse_mode='HTML')
    return {'response':'Success.'}