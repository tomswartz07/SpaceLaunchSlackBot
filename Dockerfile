FROM python:3.10.2-alpine
LABEL org.opencontainers.image.source=https://github.com/tomswartz07/SpaceLaunchSlackBot
LABEL org.opencontainers.image.authors="tom+docker@tswartz.net"
LABEL description="Docker container to run a Slack bot which posts daily \
launches obtained from LaunchLibrary."


COPY crontab .
RUN crontab crontab
COPY launch.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "crond", "-f" ]
