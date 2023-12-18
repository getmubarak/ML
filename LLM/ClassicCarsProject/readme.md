# step 1 - copy project
copy the project to your local system

# step 2 - build from the project directory
docker  build . -t classic_cars:latest

# Step 3 - run
docker run -d --name classic_cars -p 8080:8080 --network example-app classic_cars:latest 


# Step 3 - use the app
open url http://localhost:8080
