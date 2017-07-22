# PiCloud

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7dd28ce2d89d414996e3245aff7e819d)](https://www.codacy.com/app/Quilliam/PiCloud?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Wyvarn/PiCloud&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/Wyvarn/PiCloud.svg?branch=master)](https://travis-ci.org/Wyvarn/PiCloud)
[![CircleCI](https://circleci.com/gh/Wyvarn/PiCloud.svg?style=svg)](https://circleci.com/gh/Wyvarn/PiCloud)
[![codecov](https://codecov.io/gh/Wyvarn/PiCloud/branch/master/graph/badge.svg)](https://codecov.io/gh/Wyvarn/PiCloud)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7dd28ce2d89d414996e3245aff7e819d)](https://www.codacy.com/app/Quilliam/PiCloud?utm_source=github.com&utm_medium=referral&utm_content=Wyvarn/PiCloud&utm_campaign=Badge_Coverage)
[![Code Health](https://landscape.io/github/Wyvarn/PiCloud/master/landscape.svg?style=flat)](https://landscape.io/github/Wyvarn/PiCloud/master)

Upload data directly to your hard drive from wherever!

## Running the app

This application is best run in a VM, so please ensure you have [Vagrant](https://www.vagrantup.com/) installed. A VM is used to ensure there is a level playing field for all developers when running and creating the application. Although this is a nice to have, another setup invovles having docker installed, which is what the application has been built on top of.

You will find a vagrant file and a provision script which will contain all necessary tools for the VM. The VM used is `ubuntu/trusty64`.

``` sh
$ vagrant up
```
> This starts up the VM and will automatially provision it.

``` sh
$ vagrant ssh
```
> logs you into the VM

Once you are logged in you will already have all the necessary tools setup to run the application. This includes docker and docker compose.


``` sh
$ cd /vagrant
$ docker-compose build
```

> get into the shared directory and run docker compose command which will build the containers from the images already setup in the directories

And that is it, now you can run the application.

``` sh
$ docker-compose up
```
>  This will run the multi container application in the foreground and you should be able to see the output in your console

## Tests

Running tests can be done within the separate directories. The major setups are client and server. 

For running server tests

``` sh
# first stop the docker-compose up command, if it is still running with CTRL^C
$ cd server
$ pip install -r requirements.txt
(venv) $ python manage.py test
```
> Will run all the tests and print a coverage report

The coverage reports will be printed to stdout and both HTML and XML reports will be generated.

The same applies for client side tests

```bash
$ cd client
$ npm install
# if using yarn
$ yarn install
$ yarn test
```
> which will run tests in the __tests__ directory

More information can be found in individual README.md files for both client and server


Enjoy!
