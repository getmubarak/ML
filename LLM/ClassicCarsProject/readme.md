docker  build . -t classic_cars:latest

docker run -d --name classic_cars -p 8080:8080 --network example-app classic_cars:latest 
