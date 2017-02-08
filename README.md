# uploader

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7dd28ce2d89d414996e3245aff7e819d)](https://www.codacy.com/app/Quilliam/uploader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Quilliam/uploader&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/Wyvarn/uploader.svg?branch=master)](https://travis-ci.org/Wyvarn/uploader)
[![CircleCI](https://circleci.com/gh/Wyvarn/uploader.svg?style=svg)](https://circleci.com/gh/Wyvarn/uploader)
[![codecov](https://codecov.io/gh/Wyvarn/uploader/branch/master/graph/badge.svg)](https://codecov.io/gh/Wyvarn/uploader)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7dd28ce2d89d414996e3245aff7e819d)](https://www.codacy.com/app/Quilliam/uploader?utm_source=github.com&utm_medium=referral&utm_content=Quilliam/uploader&utm_campaign=Badge_Coverage)
[![Code Health](https://landscape.io/github/Wyvarn/uploader/master/landscape.svg?style=flat)](https://landscape.io/github/Wyvarn/uploader/master)

Raspberry pi cloud

Upload data directly to your hard drive!

## Running the app

This application is best run in a VM, so please ensure you have [Vagrant](https://www.vagrantup.com/) installed. A VM is used to ensure there is a level playing field for all developers when running and creating the application.

You will find a vagrant file and a provision script which will contain all necessary tools for the VM. The VM used is `ubuntu/trusty64`.

``` sh
$ vagrant up
```
> This starts up the VM and will automatially provision it.

``` sh
$ vagrant ssh
```
> logs you into the VM

``` sh
$ cd /vagrant
$ . venv/bin/activate
```
> get into the shared directory and activate the virtual environment

And that is it, now you can run the application.

``` sh
$ python manage.py runserver
```

## Tests

Running tests can be done with:

``` sh
$ python manage.py test
```
> Will run all the tests and print a coverage report

The coverage reports will be printed to stdout and both HTML and XML reports will be generated.

Enjoy!
