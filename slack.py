import requests
import json


def send_message_to_slack_channel(
    url, text, author_name, title, color):
    data = {
        "text": text,
        "attachments": [
            {
                "author_name": author_name,
                "text": text,
                "color": color,
                "fields": [{"title": title, "short": "false"}],
            },
        ],
    }
    headers = {"Content-type": "application/json"}
    if url is not None:
        # skip when short url
        if len(url) > 15:
            requests.post(url, data=json.dumps(data), headers=headers)