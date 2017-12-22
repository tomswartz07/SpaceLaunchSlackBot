#!/usr/bin/env python

"""
This script will query for upcoming rocket launches and post results to Slack
"""

import sys
import json
import datetime
import requests

# Set the webhook_url to the one provided by Slack when you create
# the webhook at https://my.slack.com/services/new/incoming-webhook/
SLACK_WEBHOOK = "<WEBHOOK URL HERE>"

API_BASE = "https://launchlibrary.net/1.3/"
# Grab next 5 launches
# We'd be living in the future if there are >5 in a day
NEXT_LAUNCH = API_BASE + "launch/next/5"

def generatepayload():
    """
    Parse out the data and create a JSON payload for Slack
    """
    r = requests.get(NEXT_LAUNCH)

    # Return None if the request was unsuccessful
    if r.status_code != requests.codes.ok:
        return None

    # Get JSON output
    data = r.json()

    launch_data = data["launches"]

    # Count the number of launches today
    launchCount = len(launch_data)
    currentUTC = datetime.datetime.utcnow()
    for launch in launch_data:
        launch_time = launch["netstamp"]
        if datetime.datetime.fromtimestamp(launch_time) <= currentUTC + datetime.timedelta(hours=24):
            launchCount -= 1
    if launchCount == 0:
        sys.exit()
    datetime.timedelta(hours=0)

    # Create payload skeleton
    if launchCount > 1:
        payload = {"text": str(launchCount) + " launches scheduled in next 24h", "attachments": []}
    else:
        payload = {"text": str(launchCount) + " launch scheduled in next 24h", "attachments": []}

    counter = 0
    for launch_data in data["launches"]:
        if counter < launchCount:
            # Extract primary launch agency
            agency = launch_data["rocket"]["agencies"][0]

            # Check if there is mission info available
            mission = "No Mission Info Available"
            for mission in launch_data["missions"]:
                mission = launch_data["missions"][0]["description"]
                mission_type = launch_data["missions"][0]["typeName"]

            image = ""
            if "placeholder" not in launch_data["rocket"]["imageURL"]:
                image = launch_data["rocket"]["imageURL"]

            # generate the launch info attachment
            payload["attachments"].append({
                "fallback": "Information",
                "color": "good",
                "author_name": agency["name"],
                "author_link": agency["infoURL"],
                "author_icon": "https://cdn4.iconfinder.com/data/icons/whsr-january-flaticon-set/512/rocket.png",
                "title": launch_data["name"],
                "text": mission,
                "image_url": image,
                "fields": [
                    {
                        "title": "Launch Location",
                        "value": launch_data["location"]["name"],
                        "short": True
                    },
                    {
                        "title": "Launch Window",
                        "value": str(datetime.timedelta(seconds=(launch_data["westamp"] - launch_data["wsstamp"]))),
                        "short": True
                    },
                    {
                        "title": "Mission Type",
                        "value": mission_type,
                        "short": True
                    }
                ],
                "footer": "Expected Launch Time",
                "footer_icon": "",
                "ts": launch_time,
                "actions": []
            })

            # Attach video buttons
            # check if there is a video stream available
            for item in launch_data["vidURLs"]:
                video = item
                payload["attachments"][counter]["actions"].append({
                    "type": "button",
                    "name": "LaunchStream",
                    "text": "Video Stream ",
                    "style": "primary",
                    "url": video
                })
            counter += 1

    return json.dumps(payload)

def postdata(message_payload):
    """
    Send json message payload to Slack webhook
    """
    requests.post(
        SLACK_WEBHOOK,
        data=message_payload,
        headers={"Content-Type": "application/json"}
    )

message = generatepayload()
postdata(message)
