import requests
from copy import copy
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.views.debug import ExceptionReporter


class SlackExceptionHandler(AdminEmailHandler):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        super(SlackExceptionHandler, self).__init__()

    def emit(self, record, *args, **kwargs):
        try:
            request = record.request
            subject = '%s (%s IP): %s' % (
                record.levelname,
                ('internal' if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS
                 else 'EXTERNAL'),
                record.getMessage()
            )
        except Exception:
            subject = '%s: %s' % (
                record.levelname,
                record.getMessage()
            )
            request = None
        subject = self.format_subject(subject)

        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        end_of_trace = reporter.get_traceback_data()['frames'][-1]
        message = '\n'.join(["{} {}".format(exc_info[0].__name__, exc_info[1]),
                             "{} line: {}".format(end_of_trace['filename'], str(end_of_trace['lineno']))])

        attachments = [
            {
                'title': subject,
                'color': 'danger',
                'text': message
            }
        ]

        data = {'attachments': attachments}

        # send it
        requests.post(self.webhook_url, json=data)
