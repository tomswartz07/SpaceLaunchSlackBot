#!/usr/bin/env python

"""
This script will query for upcoming rocket launches and post results to Slack
"""

import os
import sys
import json
import datetime
import requests

# Set the webhook_url to the one provided by Slack when you create
# the webhook at https://my.slack.com/services/new/incoming-webhook/
print(f'Running now {datetime.datetime.now()}')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')

# Dev
#NEXT_LAUNCH = "https://lldev.thespacedevs.com"
# Prod
NEXT_LAUNCH = "http://ll.thespacedevs.com"

# API Version
NEXT_LAUNCH += "/2.1.0/"

# Grab next 5 launches
# We'd be living in the future if there are >5 in a day
NEXT_LAUNCH += "launch/upcoming/?"

# Omit the launches that occurred in the past 24h
# since this script should run daily-ish
NEXT_LAUNCH += "hide_recent_previous=true"

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
    launch_data = data["results"]

    # Count the number of launches today
    launchCount = len(launch_data)
    for launch in launch_data:
        if datetime.datetime.utcnow() <= \
                datetime.datetime.strptime(launch["net"], "%Y-%m-%dT%H:%M:%SZ") <= \
                datetime.datetime.utcnow() + datetime.timedelta(hours=24):
            continue
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
    for launch_data in data["results"]:
        if counter < launchCount:
            # Extract primary launch agency
            agency = launch_data["launch_service_provider"]

            # Check if there is mission info available
            mission = "No Mission Info Available"
            for mission in launch_data["mission"]:
                mission = launch_data["mission"]["description"]
                mission_type = launch_data["mission"]["type"]

            image = ""
            image = launch_data["image"]

            liftoff_ts = ""
            footer = ""
            if launch_data["net"] != 0:
                footer = "Expected Launch Time"
                liftoff_ts = (datetime.datetime.strptime(
                    launch_data["net"], "%Y-%m-%dT%H:%M:%SZ") - \
                            datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)


            window_start = datetime.datetime.strptime(launch_data["window_start"], "%Y-%m-%dT%H:%M:%SZ")
            window_end = datetime.datetime.strptime(launch_data["window_end"], "%Y-%m-%dT%H:%M:%SZ")
            # generate the launch info attachment
            payload["attachments"].append({
                "fallback": "Information",
                "color": "good",
                "author_name": agency["name"],
                "author_link": agency["url"],
                "author_icon": "https://cdn4.iconfinder.com/data/icons/whsr-january-flaticon-set/512/rocket.png",
                "title": launch_data["name"],
                "text": mission,
                "image_url": image,
                "fields": [
                    {
                        "title": "Launch Location",
                        "value": launch_data["pad"]["location"]["name"],
                        "short": True
                    },
                    {
                        "title": "Launch Window",
                        "value": str(window_end - window_start),
                        "short": True
                    },
                    {
                        "title": "Mission Type",
                        "value": mission_type,
                        "short": True
                    }
                ],
                "footer": footer,
                "footer_icon": "",
                "ts": liftoff_ts,
                "actions": []
            })

            # Attach video buttons
            # check if there is a video stream available
            if launch_data["webcast_live"]:
                for item in launch_data["webcast_live"]:
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
