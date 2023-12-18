# step 1 - copy project
copy the project to your local system

# step 2 - build from the project directory
docker  build . -t classic_cars:latest

# Step 3 - run
docker run -d --name classic_cars -p 8080:8080 --network example-app classic_cars:latest 


<br/>
note: </br>
you should have run before step 3</br>
 docker network create example-app </br>
you should have mysql running in that network

# Step 4 - use the app
open url http://localhost:8080
