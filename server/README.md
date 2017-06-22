# PiCloud Server

This is the PiCloud server and will/can run in a docker container. The instructions for setting it up in a docker container are outlined in the [DockerFile](./Dockerfile).

These instructions create an image of the PiCloud server and expose a port for other applications to use it. In this case, we want to expose this port to the [client](../client).

## Setting up

You will obviously need docker set up on your machine. Or if you do not want docker on your machine. Simply follow the setup instuctions [here](../README.md) and setup Vagrant and in your guest OS, install docker and the application should run the same. Remember, if you follow this route, you must expose ports on the guest OS to the host OS, these ports must be the same as the ports that the docker containers will run, this is just to enable you to view the application from your host machine.

Once you have docker setup, then you can build this container from this image with

``` bash
docker build -t picloud:server:latest .
```

This will start by pulling the base image from docker hub (if you do not have it) and then setup the application code to that container following the instructions from the Dockerfile

Now you can run the container with

```bash
docker run -p 5000:5000 picloud:server
```
> This will run the app on port 5000 in the container and expose it on port 5000 on your machine

