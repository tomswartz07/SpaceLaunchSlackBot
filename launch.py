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

def generatepayload():
    """
    Parse out the data and create a JSON payload for Slack
    """
    global PAYLOAD
    r = requests.get(NEXT_LAUNCH)
    if r.status_code == requests.codes.ok:
        data = json.loads(r.text)

        agency = data["launches"][0]["rocket"]["agencies"][0]["name"]
        agency_url = data["launches"][0]["rocket"]["agencies"][0]["infoURL"]
        launch_name = data["launches"][0]["name"]
        launch_pad = data["launches"][0]["location"]["name"]
        launch_time = data["launches"][0]["net"]
        launch_timestamp = str(data["launches"][0]["netstamp"])
        mission_description = data["launches"][0]["missions"][0]["description"]
        mission_type = data["launches"][0]["missions"][0]["typeName"]
        rocket_image = data["launches"][0]["rocket"]["imageURL"]
        videos = data["launches"][0]["vidURLs"]
        launch_window = str(datetime.timedelta(
            seconds=(data["launches"][0]["westamp"] - data["launches"][0]["wsstamp"])
        ))
        try:
            video = "<" + videos[0] + "|Video Stream>"
        except Exception:
            video = "No Video Stream Available"
        PAYLOAD = "{\"attachments\":[{\"fallback\":\"" + agency + " rocket launch happening soon\",\"color\":\"good\",\"pretext\":\"" + agency + " launch scheduled for " + launch_time + "\",\"author_name\":\"" + agency + "\",\"author_link\":\"" + agency_url + "\",\"author_icon\":\"https://cdn4.iconfinder.com/data/icons/whsr-january-flaticon-set/512/rocket.png\",\"title\":\"" + launch_name + "\",\"title_link\":\"" + video + "\",\"text\":\"" + mission_description + "\",\"image_url\":\"" + rocket_image + "\",\"thumb_url\":\"\"},{\"fallback\":\"Information\",\"title\":\"Launch Information\",\"fields\":[{\"title\":\"Agency\",\"value\":\"" + agency + "\",\"short\":true},{\"title\":\"Launch Location\",\"value\":\"" + launch_pad + "\",\"short\":true},{\"title\":\"Mission Type\",\"value\":\"" + mission_type + "\",\"short\":true},{\"title\":\"Launch Window\",\"value\":\"" + launch_window + "\",\"short\":true},{\"title\":\"Live Stream Link\",\"value\":\"" + video + "\"}],\"footer\":\"Expected Launch Time\",\"footer_icon\":\"\",\"ts\":" + launch_timestamp + "}]}"
        # If you wish, you can test the payload formatting at:
        # https://api.slack.com/docs/messages/builder
        # just print(PAYLOAD) and then paste it there
        print(PAYLOAD)
        return PAYLOAD

def postdata(PAYLOAD):
    requests.post(
        SLACK_WEBHOOK,
        data=PAYLOAD,
        headers={"Content-Type": "application/json"}
    )

generatepayload()
postdata(PAYLOAD)
