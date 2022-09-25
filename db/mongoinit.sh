# DO NOT run this in prod! please update to a secure password!
docker run --name mongodb -d -p 27017:27017 --net chat-app -e MONGO_INITDB_ROOT_USERNAME=dev -e MONGO_INITDB_ROOT_PASSWORD=devapp mongo