import pymsteams
from logging import Handler
from urllib.parse import urlencode

class TeamsExceptionHandler(Handler):
    def __init__(self, webhook_url, ):
        self.webhook_url = webhook_url
        super(TeamsExceptionHandler, self).__init__()

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
            teams_message = pymsteams.connectorcard(self.webhook_url)
            teams_message.title(f'Error experienced by {user}')
            teams_message.text(msg)
            teams_message.send()

        except Exception:
            self.handleError(record)
