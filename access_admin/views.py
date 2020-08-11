import firebase_admin
import pyrebase

from django.contrib import auth
from django.shortcuts import render, redirect
from firebase_admin import firestore

from .forms import DoctorForm
from .services import must_login

config = {
    'apiKey': "AIzaSyA6REuorh5MHh7P-FEyqCImvcgQLJ6diVc",
    'authDomain': "access-8eaac.firebaseapp.com",
    'databaseURL': "https://access-8eaac.firebaseio.com",
    'projectId': "access-8eaac",
    'storageBucket': "access-8eaac.appspot.com",
    'messagingSenderId': "606957447439",
    'appId': "1:606957447439:web:52618006d76ad5ec5af67a"
}

firebase_admin.initialize_app()

firebase = pyrebase.initialize_app(config)

firebase_auth = firebase.auth()
db = firestore.client()


# ############################################################
#                           AUTH VIEWS
##############################################################


def register(request):
    if request.method == 'POST':
        # TODO: Use a form and perform validation
        first_name = request.POST['first_name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = firebase_auth.create_user_with_email_and_password(email, password)

            firebase_auth.sign_in_with_email_and_password(email, password)

            data = {
                'firstName': first_name,
                'surname': surname,
            }

            db.collection('users').document(user['localId']).set(data)

            return redirect('access_admin:index')

        except:
            context = {
                'message': 'Failed to register. Please try again'
            }
            return render(request, 'auth/register.html', context)

    else:
        return render(request, 'auth/register.html')


def sign_in(request, next_to):
    if request.method == 'POST':
        # TODO: Implement validation using forms
        email = request.POST['email']
        password = request.POST['password']

        # try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        print('==========================')
        print(user)
        # auth.login(request, )

        session_id = user['idToken']
        request.session['logged_in'] = True
        request.session['uid'] = str(session_id)
        user_details = db.collection('users').document(user['localId']).get()
        if user_details.exists:
            # request.session['first_name'] = user_details.to_dict()['firstName']
            # request.session['surname'] = user_details.to_dict()['surname']

            return redirect('access_admin:index')

        # except:
        #     message = 'Invalid credentials'
        #     context = {
        #         'message': message
        #     }
        #
        #     return render(request, 'auth/sign_in.html', context)

    else:
        return render(request, 'auth/sign_in.html')


def sign_out(request):
    del request.session['logged_in']

    return redirect('access_admin:sign_in')


@must_login
def index(request):
    context = {
        'name': 'Raymond',
        'surname': 'Jowa'
    }
    return render(request, 'access_admin/index.html', context)


# ############################################################
#                           DOCTOR VIEWS
##############################################################

@must_login
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            title = form.cleaned_data['title']
            # gender = form.changed_data['gender']
            # date_of_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['address']
            suburb = form.cleaned_data['suburb']
            city = form.cleaned_data['city']
            phone1 = form.cleaned_data['phone1']
            phone2 = form.cleaned_data['phone2']
            email = form.cleaned_data['email']

            print(f'name - {first_name}')
            print(f'title - {title}')
            # print(f'gender - {gender}')

            # TODO: Process data here
            return redirect('access_admin:index')  # TODO build view doctor and redirect there

    else:
        form = DoctorForm()

    return render(request, 'access_admin/add_doctor.html', {'doctor_form': form})
