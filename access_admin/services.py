
from django.shortcuts import redirect


def must_login(function):

    def wrapper(*args, **kwargs):

        request = args[0]

        logged_in = request.session.get('logged_in', False)

        if logged_in:
            return function(*args)
        else:
            return redirect('access_admin:sign_in')

    return wrapper


def doctor_required(function,):
    def wrapper(*args, **kwargs):
        request = args[0]
        types = request.session.get('types', [])
