# Space Launch Slack Bot

This repository contains the code for a script that will post information regarding upcoming space launches to a custom Slack Channel.

**What It Does:** Post information about upcoming space launches to your Slack Channel

**What It Does Not:** Fulfill your hopes and dreams (unless your hopes and dreams were to post information about space launches to your Slack Channel)

## Setup
### Prerequisites
- Python 3
- Working Internet Connection
- Admin Access to a Slack Team or the ability to bribe someone who does

### Implementation
1. Create a new [Incoming Slack Webhook](https://api.slack.com/incoming-webhooks)
  - Feel free to customize it as you wish.
  - If you don't have access to add an incoming webhook, see the [Recommended Settings](#recommended-settings) section for more details.
2. Dump webhook url into the copy of the script if running directly. (See [Docker](#running-in-docker) section below if running in Docker)
  - Webhook goes in the `SLACK_WEBHOOK` variable
3. Run that shit. Schedule a cron job or put it in Kubernetes or something. I don't know.

## Recommended Settings
When creating the custom webhook for the Slack channel, there are a few options to customize.

It's also possible that you don't have access to add an incoming webhook to your team because of the permissions model. In that case, you would need to know what to send to the admin to get it set up. This is that stuff.

Here are the recommended settings when setting up the Hook:
- **Post to Channel:** Your `#space` channel, or `#rockets`
- **Descriptive Label:** Whatever you want. This isn't really necessary.
- **Customize Name:** "Upcoming Launches"
- **Customize Icon:** Pick an emoji → `:rocket:` :rocket:

Copy the Webhook URL or have the Admin send that URL to you, you'll need it for the script.

## Running
The bot will run and post the details of the next rocket launch, as determined via info from [LaunchLibrary](http://launchlibrary.net/)

## Running in Docker

Since this script is fairly simple, it's easy enough to run in a compact docker
container, ensuring that the script is offloaded from whatever main host you have.

### Building Docker Image
There is a GitHub action which will build and deploy this container automatically,
but if you want to build it locally (i.e. to use a custom cron schedule)

1. Edit the `crontab` file to reflect the schedule you want. By default, it will
run at 7am daily. (Be sure to set the `TZ` env var to your local time, otherwise
UTC will be used)

2. Build the image
```
docker build -t slack-launch .
```

3. Run the image
```
docker run -it --detach --rm --name slack-launch -e TZ="America/New_York" -e SLACK_WEBHOOK='https://hooks.slack.com/services/HOOKURL' slack-launch
```

## Contributing

Check out the Issues page for a list of potential tasks and features that are on the roadmap to be added.
Once you select an issue or feature that you would like to work on, please assign yourself that issue.
