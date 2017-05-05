#!/usr/bin/env python

"""
This script will query for upcoming rocket launches and post results to Slack
"""

import json
import datetime
import requests

# Set the webhook_url to the one provided by Slack when you create
# the webhook at https://my.slack.com/services/new/incoming-webhook/
SLACK_WEBHOOK = "<WEBHOOK URL HERE>"

API_BASE = "https://launchlibrary.net/1.2/"
NEXT_LAUNCH = API_BASE + "launch/next/1"

"""
Parse out the data and create a JSON payload for Slack
"""
def generatepayload():
    r = requests.get(NEXT_LAUNCH)

    # return None if the request was unsuccessful
    if r.status_code != requests.codes.ok:
        return None

    # get json output
    data = r.json()

    # extract some heavily used objects
    launch_data = data["launches"][0]
    agency = launch_data["rocket"]["agencies"][0]

    # check if there is a video stream available
    video = "No Video Stream Available"
    if len(launch_data["vidURLs"]) > 0:
        video = "<" + launch_data["vidURLs"][0] + "|Video Stream>"

    # bare bones payload
    payload = {"attachments": []}

    # generate the rocket info attachment
    payload["attachments"].append({
        "fallback": agency["name"] + " rocket launch happening soon",
        "color": "good",
        "pretext": agency["name"] + " launch scheduled for " + launch_data["net"],
        "author_name": agency["name"],
        "author_link": agency["infoURL"],
        "author_icon": "https://cdn4.iconfinder.com/data/icons/whsr-january-flaticon-set/512/rocket.png",
        "title": launch_data["name"],
        "title_link": video,
        "text": launch_data["missions"][0]["description"],
        "image_url": launch_data["rocket"]["imageURL"]
    })

    # generate the launch info attachment
    payload["attachments"].append({
        "fallback": "Information",
        "title": "Launch Information",
        "fields": [
            {
                "title": "Agency",
                "value": agency["name"],
                "short": True
            },
            {
                "title": "Launch Location",
                "value": launch_data["location"]["name"],
                "short": True
            },
            {
                "title": "Mission Type",
                "value": launch_data["missions"][0]["typeName"],
                "short": True
            },
            {
                "title": "Launch Window",
                "value": str(datetime.timedelta(seconds=(launch_data["westamp"] - launch_data["wsstamp"]))),
                "short": True
            },
            {
                "title": "Live Stream Link",
                "value": video
            }
        ],
        "footer": "Expected Launch Time",
        "footer_icon": "",
        "ts": launch_data["netstamp"]
    })

    return json.dumps(payload)

"""
Send json message payload to Slack webhook
"""
def postdata(message_payload):
    requests.post(
        SLACK_WEBHOOK,
        data=message_payload,
        headers={"Content-Type": "application/json"}
    )

message_payload = generatepayload()
postdata(message_payload)
