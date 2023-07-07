FROM node
WORKDIR /DisneyPlus/frontend/

COPY . /DisneyPlus/frontend/

CMD npm install -l; npm start