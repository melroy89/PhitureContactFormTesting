# Example of Running selenium inside docker
This repo setup a python docker image with Selenium setup for both Firefox and Chrome browsers including Chromedriver and Geckodriver setup. This image is intented for scripts which selenium and need to be run on Google Cloud Run.


### Available browsers
 * Firefox
 * Chrome

## Selenium documentaion
https://selenium-python.readthedocs.io/

## pyvirtualdisplay documentation
https://github.com/ponty/pyvirtualdisplay/tree/3.0


# Setup
docker build  -t phiture_docker_selenium .
