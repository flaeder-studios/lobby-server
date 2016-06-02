echo Launching multipong server on 127.0.0.1:5000

docker stop multipong
docker rm multipong
docker run --rm -t -p 5000:5000 --name multipong multipong-server
