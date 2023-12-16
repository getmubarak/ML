docker network create example-app

docker run -p 8888:8888 --privileged  -e GRANT_SUDO=yes --user root --network example-app  -v /Users/mubarak/Documents/deck/ML/ml_demos:/home/jovyan/work jupyter/scipy-notebook 

-p 8888:8888: Exposes the server on host port 8888
 --privileged 
-v <your working directory>:/home/jovyan/work: Mounts the working directory on the host as /home/jovyan/work folder in the container to save the files between your host machine and a container.
-e JUPYTER_ENABLE_LAB=yes: Run JupyterLab instead of the default classic Jupyter Notebook.
--name notebook: Define a container name as notebook
-it: enable interactive mode with a pseudo-TTY when running a container
--env-file .env: Pass a .env file to a container


$ docker ps

$ docker run --name mysql  --privileged  -e GRANT_SUDO=yes --user root  --network example-app  -v /Users/mubarak/Documents/deck/ML/ml_demos/LLM:/var/lib/mysql  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=abc --restart unless-stopped mysql

$ sudo docker cp /Users/mubarak/Documents/deck/ML/ml_demos/LLM/mysqlsampledatabase.sql 141b253b9656:/

$ docker exec -it 8b8a101bf869 /bin/bash

$ mysql -u root -p
  abc

$ source mysqlsampledatabase.sql

$ show databases;

remove all stopped containers
$ docker rm $(docker ps --filter status=exited -q)
