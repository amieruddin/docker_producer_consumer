# docker_producer_consumer
Send JSON data through docker container


1. OS : Linux Ubuntu 20.04

2. configure docker
$ sudo apt-get update
$ sudo apt install docker.io
$ sudo snap install docker
$ docker --version
$ pip install docker-compose

3. configure rabbitmq
$ sudo chmod 666 /var/run/docker.sock

4. create environment
$ conda create --name tapway python=3.7
$ pip install -r requirements

5. run docker-compose



