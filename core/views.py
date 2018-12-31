import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Application, Client, Notification, handle_notification
from .utils import get_token, get_error_res, get_success_res
from allauth.account.forms import LoginForm, SignupForm

# Create your views here.
"""
routes to create : 
/registerusers : { app_token: '', users: [ user_id,... ] } POST
/notify : {app_token:'', users: [user_id,....], content: 'JSON{}' }
"""


def hello(request):
    ctx = {
        'login_form': LoginForm(),
        'signup_form': SignupForm()
    }
    return render(request, 'webapp/landing.html', ctx)


@csrf_exempt
def register_users(request):
    """
    Used to register a list of user for one application it should be used to register. it take argument with POST
    like { 'app_token': '', 'users': [user_id, user_id, ...] }.
    :param request:
    :return:
    """
    _token = get_token(request.POST)
    if not _token:
        return get_error_res('No app_token provided  unable to bind this request to any registered app', 403)
    # get the concerned app
    app = Application.objects.filter(app_token=_token).first()
    if app:
        # save the users related to this app
        if not 'users' in request.POST:
            return get_error_res('No user\'s list provided unable to populate', 400)
        _users = json.loads(request.POST['users'])  # deserialize the users list here
        for user in _users:
            cl, created = Client.objects.get_or_create(client_id=user, app=app)
            cl.save()  # save him here
        return get_success_res('Users registered with success')
    else:
        return get_error_res('No application detected with the app_token, maybe you should create it first', 404)


@csrf_exempt
def notify(request):
    """
    To send one notification to one or many user, it take the app_token , the notification content and the list of
    concerned users.

    The users are only represented by theirs ids

    :param request:
    :return:
    """
    _token = get_token(request.POST)
    if not _token:
        return get_error_res('No app_token provided  unable to bind this request to any registered app', 403)
    # get the concerned app
    app = Application.objects.filter(app_token=_token).first()
    if app:
        if not 'users' in request.POST:
            return get_error_res('No user\'s list provided unable to perform notifications', 400)

        if not 'content' in request.POST:
            return get_error_res('No content provided unable to perform notifications', 400)
        _users = json.loads(request.POST['users'])  # deserialize the users list here
        clients = Client.objects.filter(client_id__in=list(_users), app=app)  # retrieve users which are related to the
        # app and which has been send in the query, now we have clients which should be notified
        _content = json.loads(request.POST['content'])
        notification = Notification(content=_content, application=app)
        notification.save()
        for cl in clients:
            print(cl)
            notification.clients.add(cl)  # connect the client to the notification
        print(notification.clients.all())

        handle_notification(notification, True)
        return get_success_res('Notifications send with success with success')
    else:
        return get_error_res('No application detected with the app_token, maybe you should create it first', 404)


def testpage(request):
    return render(request, 'core/index.html', {})
