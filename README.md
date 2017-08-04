# baseruntime-docker-tests
CI Tests for the Base Runtime docker image

How to run a test using the [avocado testing framework](http://avocado-framework.github.io/):

    $ avocado run $TEST.py [ --mux-inject 'run:$TESTPARAM:$VALUE' ... ]

## Setup

### Package setup

Install prerequisite RPMs if necessary:

* mock - Builds packages inside chroots
* python2-configparser - Configuration file parser

        $ sudo dnf install mock python2-configparser

* meta-test-family - Meta test family

        $ sudo dnf copr enable phracek/meta-test-family
        $ sudo dnf install meta-test-family

### Mock setup

Add your user to the mock group:

    $ sudo usermod -aG mock $USER

### Docker setup

[Configure docker to run as your (non-root!) userid](https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user):

    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER

[Configure docker to start automatically (and start it)](https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user#configure-docker-to-start-on-boot):

    $ sudo systemctl enable docker
    $ sudo systemctl start docker

### Group membership setup

Log out and log back in so that your group membership is re-evaluated.

### Sudo setup

Add the following lines to /etc/sudoers or put them into a new file such as /etc/sudoers.d/mock-tar-chroot:

    %mock ALL=(root) NOPASSWD: /usr/bin/tar -C /var/lib/mock/*/root -c .,\
                               !/usr/bin/tar -C /var/lib/mock/* */root -c .,\
                               /usr/bin/tee /var/lib/mock/*/root/etc/dnf/dnf.conf,\
                               !/usr/bin/tee /var/lib/mock/* */root/etc/dnf/dnf.conf


The above configuration allows members of the 'mock' group to generate a complete docker image. An image can still be created without performing this step, but it will be incomplete and the test setup phase will finish with a warning.

## Background

Avocado starts a fresh process per test method and runs setup/teardown methods
each time. We can't afford to have that cause our docker image be repeatedly
created/removed. Thus, these CI tests have been split up into three phases:
* setup: creates the docker image
* smoke: runs the tests
* teardown: removes the docker image

## Running these tests

Run each of the phases in sequence. e.g.,

    $ avocado run ./setup.py
    $ avocado run ./smoke.py
    $ avocado run ./teardown.py

In the future, additional test scripts can be run between the setup and teardown.

### Setting docker image name parameter

All of the scripts need to know the name to use for the base-runtime docker image. The scripts will use modularity test framework to get the image name.
There are 2 options to set the image name. The first is to define it on config.yaml file. The second one is to set URL env variable, this will override the name from the config file.
* Example:

        $ export URL="docker=base-runtime-smoke"
        $ avocado run ./setup.py
        $ avocado run ./smoke.py
        $ avocado run ./teardown.py

## Test script configuration overrides

Optional test script configuration overrides can provided on the command line using [avocado's parameter passing mechanism](http://avocado-framework.readthedocs.io/en/latest/WritingTests.html#accessing-test-parameters) in the following manner:

    $ avocado run $TEST.py [ --mux-inject 'run:$TESTPARAM:$VALUE' ... ]

**Note:** When using avocado-51.0 or later, you will get an avocado run error when attempting to use the `--mux-inject` command line option unless you also have the `python2-avocado-plugins-varianter-yaml-to-mux` package installed. For more information please refer to the [avocado 51.0 release notes](http://avocado-framework.readthedocs.io/en/51.0/release_notes/51_0.html).

### mockcfg - path to mock configuration file

The setup.py and teardown.py scripts need to read a base-runtime mock configuration file. The default path is 'resources/base-runtime-mock.cfg' relative to the directory where the test script resides. This path can be overridden with the 'mockcfg' parameter.

### compiler-test-dir - path to compiler test resource directory

The smoke.py script needs to access a base-runtime compiler test resource directory. The default path is 'resources/hello-world' relative to the directory where the test script resides. This path can be overridden with the 'compiler-test-dir' parameter.

