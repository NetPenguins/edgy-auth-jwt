# Edgy Auth JWT
### Author: [Chad Wilson](https://blog.edgystack.com/author/cmwilson919)
> FastAPI based authentication microservice using JWT and Basic HTTP authentication example.
---
### Get Started
> A Visual Studio code dev container is available for quick startup. For more information on the dev container setup and startup take a look at their [docs](https://code.visualstudio.com/docs/remote/containers)
### Docker network
In order to follow along with minimal changes you will need to run the following to setup a new docker network. 
```sh
docker network create chat-app
```

### MongoDB 
You will need to have a mongodb instance running in docker or host your own. To spin up a quick instance in docker run the following:
```sh
docker run --name mongodb -d -p 27017:27017 --net chat-app -e MONGO_INITDB_ROOT_USERNAME=dev -e MONGO_INITDB_ROOT_PASSWORD=devapp mongo
```
> Additionally you can use the `.env` file provided in the root directory to update/set mongoDB information

### Run the App
In a terminal/shell run the following: 

```sh
# Setup a virtualenv
python3 -m venv venv

# Install the python dependencies
python3 -m pip install -r requirements.txt 

# Run the app
python3 main.py
```

### Up and running
Once you are up and running you can visit the docs by going to http://localhost:<port provided>/docs or http://localhost:<port provided>/redoc
