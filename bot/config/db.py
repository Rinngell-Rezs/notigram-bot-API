from pymongo import MongoClient
from os import environ

conn = MongoClient(environ.get('mongo_URI'))

