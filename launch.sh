echo Launching flaeder lobby on /tmp/flaeder/lobby/socket

docker stop flaeder-lobby
docker rm flaeder-lobby
docker run -t --name flaeder-lobby -d flaeder-lobby
