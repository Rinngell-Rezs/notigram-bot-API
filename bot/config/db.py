from pymongo import MongoClient

creds = {
    'DB':'',
    'USER':'notigram',
    'PASSWORD':'seY3DsImx02HBjY3',
}

creds['URI'] = f'mongodb+srv://notigram:{creds["PASSWORD"]}@cluster0.dnee7co.mongodb.net/?retryWrites=true&w=majority'

conn = MongoClient(creds['URI'])