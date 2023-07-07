import os
import json
from bson import ObjectId

from backend.db import db

current_directory = os.path.dirname(os.path.abspath(__file__))

dumps = [{'name': 'users_data.json', 'collection': db.users}, {'name': 'shows_data.json', 'collection': db.shows}]


async def load_data_to_DB():
    for dump in dumps:
        file_path = os.path.join(current_directory, dump['name'])
        with open(file_path) as json_file:
            data = json.load(json_file)

            for doc in data:
                doc['_id'] = ObjectId(doc['_id']['$oid'])

            await dump['collection'].insert_many(data)
