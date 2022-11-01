import requests
import json


def send_message_to_slack_channel(
    url, text, author_name, title, color):
    data = {
        "attachments": [
            {
                "color": color,
                "author_name": author_name,
                "title": title,
                "text": text,
                "fields": [{"short": "false"}],
            },
        ],
    }
    headers = {"Content-type": "application/json"}
    if url is not None:
        # skip when short url
        if len(url) > 15:
            requests.post(url, data=json.dumps(data), headers=headers)