# Example of Running selenium inside docker
This repo set up a python docker image with Selenium setup for both Firefox and Chrome browsers including Chromedriver and Geckodriver setup. This image is intended for scripts which selenium and need to be run on GitHub Actions.


### Available browsers
 * Firefox
 * Chrome
 * Mobile version of any available browser (simply uncomment one or two lines in code)


## Selenium documentation
https://selenium-python.readthedocs.io/

## pyvirtualdisplay documentation
https://github.com/ponty/pyvirtualdisplay/tree/3.0

## slack webhooks (can be deprecated later)
https://api.slack.com/messaging/webhooks


# Setup
docker build  -t phiture_docker_selenium .

# Logs
If there is not enough information in the slack channel, you can find extra info in the docker logs or you can run it locally.
Just clone the project from GitHub, install all libraries from the requirements file and click "run".

# Contact info
Any questions? Please text via Slack or Gmail to:
-Iskandar Khanbekov 
-Abdul Majeed Alkattan
