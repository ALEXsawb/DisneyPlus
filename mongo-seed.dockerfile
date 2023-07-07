FROM mongo

COPY backend/shows_data.json /shows_data.json
COPY backend/users_data.json /users_data.json

CMD mongoimport --host mongodb --db DisneyPlus --collection shows --type json --file /shows_data.json --jsonArray && mongoimport --host mongodb --db DisneyPlus --collection users --type json --file /users_data.json --jsonArray
