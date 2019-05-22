## moderator_bot

aiohttp demo for simple Slack bot that moderate toxic messages.
It uses Events API.

Model reused from [Moderator AI](https://github.com/aio-libs/aiohttp-demos/tree/master/demos/moderator) project.

![Image of Application](/docs/_static/slack_moderator.gif)


## Requirements
 - [aiohttp](https://github.com/aio-libs/aiohttp)
 - [aioslacker](https://github.com/aio-libs/aioslacker)


## Prerequisites
Before running bot, you need to setup slack app for it and obtain `SLACK_BOT_TOKEN`. You can read detailed guide on how to do it here https://api.slack.com/bot-users.

Also you need `GIPHY_API_KEY` that you can get here https://developers.giphy.com/.

## Starting bot
Clone the repo and after do

```shell
$ cd moderator_bot
$ pip install -r requirements-dev.txt
```
With credentials from previous section provide proper environment variables

```shell
$ set -x SLACK_BOT_TOKEN xxx-xxx
$ set -x GIPHY_API_KEY xxx-xxx
```

Start app
```shell
$ python -m moderator_bot
```

## Testing
```shell
$ pytest -s tests/
```
