FROM python:latest

LABEL author="Abdul Majeed Alkattan"

WORKDIR /code

# Install requirements
COPY . /code

# Install firefox
RUN apt update && apt -y upgrade \
    && apt install -y python3-pyvirtualdisplay xvfb \
    firefox-esr unzip && pip install --upgrade pip && pip install -r requirements.txt

# Install geckodriver
RUN wget 'https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz' -O geckodriver.tar.gz \
    &&  tar xzf geckodriver.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver.tar.gz


# install Chrome
RUN wget 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' -O chrome.deb \
&& apt install ./chrome.deb -f -y


# Install Chrome driver
RUN wget "https://chromedriver.storage.googleapis.com/`curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(google-chrome --version| cut -d " " -f3|cut -d. -f 1)"`/chromedriver_linux64.zip" -O chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip && mv chromedriver /usr/local/bin/ && rm chromedriver*

CMD ["python3", "main.py"]