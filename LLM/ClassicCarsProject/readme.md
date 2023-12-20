
### step 1 - copy project
#### copy the project to your local system

### step 2 - build from the project directory
#### docker  build . -t classic_cars:latest

### step 3 - create a network
#### docker network create example-app

### step 4 - run My SQL
#### docker run --name mysql --privileged -e GRANT_SUDO=yes --user root --network example-app -p 3306:3306 -e MYSQL_ROOT_PASSWORD=abc --restart unless-stopped mysql

### step 5 - copy the script to SQL container
#### sudo docker cp /Users/mubarak/Documents/deck/ML/ml_demos/LLM/mysqlsampledatabase.sql 141b253b9656:/

### step 6 - get into the sql container
#### docker exec -it 8b8a101bf869 /bin/bash

### step 7 - run mysql inside the container
#### mysql -u root -p abc

### step 8 - import database
#### source mysqlsampledatabase.sql

### step 9 - check the db, there should be a new db called classicmodels 
#### show databases;

### step 10 - run UI Application
#### docker run --name classic_cars -p 8080:8080 --network example-app classic_cars:latest 

### Step 11 - use the app
#### open url http://localhost:8080
