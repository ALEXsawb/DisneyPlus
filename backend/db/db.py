from motor import motor_asyncio

from backend.settings import settings

SHOWS = ['StarWars', 'Marvel', ]

client = motor_asyncio.AsyncIOMotorClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = client.DisneyPlus

shows = db.shows
users = db.users


async def create_user_indexed_fields():
    await users.create_index([('email', 1), ], unique=True)


async def create_show_indexed_fields():
    await shows.create_index([('show', 1), ], unique=True)
