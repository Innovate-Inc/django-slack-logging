# django-slack-logging

Simple Slack Logging for Django

Install
```pip
pip install git+https://github.com/Innovate-Inc/django-slack-logging#egg=django-slack-logging
```

Update Django logging settings
```python
LOGGING = {
    # additional handler for slack
    'handlers': {
        'slack': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'slack_logging.SlackExceptionHandler',
        'webhook_url': '<webhook.url>'
    }
}
```

