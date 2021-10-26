FROM python:3-alpine
LABEL org.opencontainers.image.source=https://github.com/tomswartz07/SpaceLaunchSlackBot
LABEL org.opencontainers.image.authors="tom+docker@tswartz.net"
LABEL description="Docker container to run a Slack bot which posts daily \
launches obtained from LaunchLibrary."


COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN crontab crontab

CMD [ "crond", "-f" ]
