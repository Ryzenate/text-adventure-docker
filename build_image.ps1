# Clean any previous attempts
docker-compose down
write-host "press a key to build image..."
pause
write-host "building..."
docker-compose build
write-host "press a key to run..."
pause
docker-compose up
write-host "You can close this window if you want."
pause
write-host "press a key to force rebuild or EXIT."
docker-compose down
write-host "press a key to prune..."
pause
docker system prune -f
write-host "press a key to build force-recreate..."
pause
docker-compose up --build --force-recreate
write-host "well?"
pause