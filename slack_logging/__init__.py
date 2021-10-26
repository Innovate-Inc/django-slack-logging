import requests
from logging import Handler


class SlackExceptionHandler(Handler):
    def __init__(self, bot_token, channel_id, bot_username=None):
        self.bot_token = bot_token
        self.channel_id = channel_id
        if bot_username is not None:
            self.bot_username = bot_username
        super(SlackExceptionHandler, self).__init__()

    def emit(self, record):
        try:
            if record.request and not record.request.user.is_anonymous:
                user = record.request.user
            else:
                user = 'Unknown'

            msg = self.format(record)
            data = {"text": f"{record.levelname.title()} experienced by {user}", "channel": self.channel_id}
            if self.bot_username is not None:
                data['username'] = self.bot_username

            requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data=data)
            requests.post("https://slack.com/api/files.upload", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data={"content": msg, "channels": self.channel_id, "filetype": "python", "filename": "traceback.py"})

        except Exception:
            self.handleError(record)
