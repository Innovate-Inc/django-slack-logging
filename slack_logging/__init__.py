import requests
from copy import copy
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter
from logging import Handler
from io import StringIO


class SlackExceptionHandler(AdminEmailHandler):
    def __init__(self, bot_token, channel_id):
        self.bot_token = bot_token
        self.channel_id = channel_id
        super(SlackExceptionHandler, self).__init__()

    def emit(self, record):
        try:
            if record.request and not record.request.user.is_anonymous:
                user = record.request.user
            else:
                user = 'Unknown'

            msg = self.format(record)
            requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data={"text": f"{record.levelname.title()} experienced by {user}", "channel": self.channel_id})
            requests.post("https://slack.com/api/files.upload", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data={"content": msg, "channels": self.channel_id, "filetype": "python", "filename": "traceback.py"})

        except Exception:
            self.handleError(record)
