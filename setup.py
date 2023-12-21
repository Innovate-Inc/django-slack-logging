from setuptools import setup

setup(
    name='django-slack-logging',
    version='1.0.0',
    packages=['slack_logging', 'ms_teams_logging'],
    install_requires=['requests', 'pymsteams'],
    url='',
    license='',
    author='Travis Bock',
    author_email='tbock@innovateteam.com',
    description='Django Slack Logging'
)
