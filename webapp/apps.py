from django.apps import AppConfig

"""
This module will host the whole source code of the webapp used by PushBack's user,
features should be :
- creating an account (via github, facebook, google, email, etc)
- viewing a list of user's application 
- viewing list of notifications per user's application
- download client's app list in csv or json or what ever
- enable/disable app
- view stats about sended notifications
- retrieving application ID
- delete an application
"""


class WebappConfig(AppConfig):
    name = 'webapp'
