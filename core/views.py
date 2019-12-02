from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm


def hello(request):
    ctx = {
        'login_form': LoginForm(),
        'signup_form': SignupForm()
    }
    return render(request, 'webapp/landing.html', ctx)


def testpage(request):
    return render(request, 'core/index.html', {})
