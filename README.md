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
2. Dump webhook url into the copy of the script.
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

## Contributing

Check out the Issues page for a list of potential tasks and features that are on the roadmap to be added.
Once you select an issue or feature that you would like to work on, please assign yourself that issue.
