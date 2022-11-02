import requests
import json


def send_positive_message_to_slack_channel(
    url, text, title, color):
    data = {
        "attachments": [
            {
                "text": text,
                "title": title,
                "color": color,
                "fields": [{"short": "false"}],
            },
        ],
    }
    headers = {"Content-type": "application/json"}
    if url is not None:
        # skip when short url
        if len(url) > 15:
            requests.post(url, data=json.dumps(data), headers=headers)


def send_negative_message_to_slack_channel(
    url, text, title, color):
    data = {
        "attachments": [
            {
                "text": text,
                "title": title,
                "color": color,
                "fields": [{"short": "false"}],
            },
        ],
    }
    headers = {"Content-type": "application/json"}
    if url is not None:
        # skip when short url
        if len(url) > 15:
            requests.post(url, data=json.dumps(data), headers=headers)