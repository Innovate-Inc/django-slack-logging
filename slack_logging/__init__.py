import requests
from logging import Handler
from urllib.parse import urlencode

class SlackExceptionHandler(Handler):
    def __init__(self, bot_token, channel_id):
        self.bot_token = bot_token
        self.channel_id = channel_id
        super(SlackExceptionHandler, self).__init__()

    def emit(self, record):
        try:

            if hasattr(record, 'request') and not record.request.user.is_anonymous:
                user = record.request.user
                if record.request.GET:
                    params = urlencode(record.request.GET)
                    record.msg += '?%s'
                    record.args = record.args + (params,)
            elif record.pathname == 'manage.py':
                user = 'management command'
            else:
                user = 'Unknown'

            msg = self.format(record)
            requests.post("https://slack.com/api/chat.postMessage", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data={"text": f"{record.levelname.title()} experienced by {user}", "channel": self.channel_id})
            r = requests.post("https://slack.com/api/files.getUploadURLExternal", headers={"Authorization": f"Bearer {self.bot_token}"},
                             data={"filename": "traceback.py", "snippet_type": "python", "length": len(msg), })
            upload_url = r.json()["upload_url"]
            file_id = r.json()["file_id"]
            requests.post(upload_url, files={"file": ("traceback.py", msg)})
            requests.post("POST https://slack.com/api/files.completeUploadExternal", headers={"Authorization": f"Bearer {self.bot_token}"},
                          data={"files": [{"id": file_id, "title": "traceback.py"}], "channel_id": self.channel_id})

        except Exception:
            self.handleError(record)
