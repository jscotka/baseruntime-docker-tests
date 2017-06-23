"""
get configuration parameters for base runtime smoke testing
"""

import os
import logging
from moduleframework import module_framework


def get_mockcfg(self):
    """
    Get the path to the base runtime mock configuration file

    This is provided by the avocado 'mockcfg' parameter if supplied,
    otherwise it is set to "resources/base-runtime-mock.cfg" relative to
    the test script directory.
    """

    script_dir = os.path.abspath(os.path.dirname(__file__))
    self.log.info("running script from directory: %s" % script_dir)

    mockcfg = self.params.get('mockcfg', default=os.path.join(
        script_dir, "resources", "base-runtime-mock.cfg"))
    mockcfg = str(mockcfg)

    if not mockcfg.endswith(".cfg"):
        self.error("mock configuration file %s must have the extension '.cfg'" %
                   mockcfg)

    if not os.path.isfile(mockcfg):
        self.error("mock configuration file %s does not exist" %
                   mockcfg)

    self.log.info("mock configuration file: %s" % mockcfg)

    return mockcfg


def get_compiler_test_dir(self):
    """
    Get the path to the base runtime compiler test resource directory

    This is provided by the avocado 'compiler-test-dir' parameter if supplied,
    otherwise it is set to "resources/hello-world" relative to
    the test script directory.
    """

    script_dir = os.path.abspath(os.path.dirname(__file__))
    self.log.info("running script from directory: %s" % script_dir)

    compdir = self.params.get(
        'compiler-test-dir', default=os.path.join(script_dir, "resources", "hello-world"))
    compdir = str(compdir)

    if not os.path.isdir(compdir):
        self.error("Compiler test resource directory %s does not exist" % compdir)

    self.log.info("Compiler test resource directory: %s" % compdir)

    return compdir


def get_docker_image_name(self):
    """
    Get the name to use for the base runtime docker image
    """

    container_helper = module_framework.ContainerHelper()
    #It tries to get the name from URL env variable
    #If URL is not defined it tries to get the name from config.yaml
    image_name = container_helper.getDockerInstanceName()
    if not image_name:
        self.error("Could not find docker image name to use")

    self.log.info("base runtime image name: %s" % image_name)

    return image_name

def get_docker_labels(self):
    """
    From config file get the labels that should be added to the image
    """

    config = module_framework.get_config()
    if not config:
        self.error("Could not get config file")
    if 'module' not in config.keys():
        self.error("Config file does not have module section")
    if 'docker' not in config['module'].keys():
        self.error("Config file does not have docker module section")

    docker_cfg = config['module']['docker']
    if 'labels' not in docker_cfg.keys():
        return None
    return docker_cfg['labels']

def get_test_profile(self):
    """
    From config file get the labels that should be added to the image
    """

    return "container"
