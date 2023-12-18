# step 1
docker  build . -t classic_cars:latest


# Step 2
docker run -d --name classic_cars -p 8080:8080 --network example-app classic_cars:latest 


# Step 3
open url http://localhost:8080
