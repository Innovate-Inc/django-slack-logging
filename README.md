# django-slack-logging

Simple Slack Logging for Django

Install
```pip
pip install git+https://github.com/Innovate-Inc/django-slack-logging.git#egg=django-slack-logging
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
        'bot_token': '<bot_token>',
        'channel_id': '<channel_id>'
    }
}
```

Set proper scope on bot token at api.slack.com\
Under your app: Features > Oauth & Permissions > Scope > Bot Token Scopes\
Add: chat:write, chat:write.customize, files:write
