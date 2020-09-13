import datetime
import firebase_admin
import pyrebase

from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from firebase_admin import firestore

from .constants import SPECIALTIES, SPECIALTIES_DICT
from .forms import DoctorForm, DoctorSearchForm, PolicySearchForm, SpecialistForm, SpecialistSearchForm
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


def boss_dashboard(request):
    return render(request, 'access_admin/boss_dashboard.html')


# ############################################################
#                           DOCTOR VIEWS
##############################################################

@must_login
def add_doctor(request):

    # Get list of cities from database
    cities = db.collection('cities').document('cities').get().to_dict()['cities']

    # convert list to tuple of tuples
    cities_list = tuple((city, city) for city in cities)

    if request.method == 'POST':
        form = DoctorForm(request.POST, cities_list=cities_list)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            title = form.cleaned_data['title']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['address']
            suburb = form.cleaned_data['suburb']
            city = form.cleaned_data['city']
            phone1 = form.cleaned_data['phone1']
            phone2 = form.cleaned_data['phone2']
            email = form.cleaned_data['email']

            print(f'name - {first_name}')
            print(f'title - {title}')
            print(f'gender - {gender}')
            print(f'DOB - {date_of_birth}')
            print(f'city - {city}')
            print(f'suburb - {suburb}')

            combined_name = f'{title} {first_name[0]}. {surname}'

            # TODO validate age, phone number, 

            doc_ref = db.collection('doctor').document()
            doc_ref.set({
                'firstName': first_name,
                'surname': surname.upper(),
                'name': combined_name,
                'gender': gender,
                'dateOfBirth': datetime.datetime.combine(date_of_birth, datetime.time()),
                'address': address,
                'city': city,
                'phone': [phone1, phone2],
                'email': email
            })

            suburb_ref = db.collection('suburbs').document(suburb)
            suburb_ref.update({u'doctors': firestore.ArrayUnion([{
                'docid': doc_ref.id,
                'name': combined_name
            }])})

            suburb_doc = suburb_ref.get()
            sub = suburb_doc.to_dict()
            doc_ref.update({'suburb': sub['name']})

            return redirect('access_admin:index')

    else:

        form = DoctorForm(cities_list=cities_list)

    return render(request, 'access_admin/add_doctor.html', {'doctor_form': form})


def fetch_suburbs(request):
    city = request.POST.get('city', None)

    try:
        suburbs = db.collection('cities').document(city).get().to_dict()['suburbs']

        data = {
            'suburbs': suburbs
        }

    except TypeError:
        data = {
            'error_message': 'Failed to load suburb data. Please contact administrator'
        }

    return JsonResponse(data)


def search_doctor(request):

    # Get list of cities from database
    cities = db.collection('cities').document('cities').get().to_dict()['cities']

    # convert list to tuple of tuples
    cities_list = tuple((city, city) for city in cities)

    if request.method == 'POST':
        form = DoctorSearchForm(request.POST, cities_list=cities_list)
        if form.is_valid():
            surname = form.cleaned_data['surname'].upper()
            city = form.cleaned_data['city']
            suburb = form.cleaned_data['suburb']
            end_surname = surname + 'z'

            if suburb == '':
                query = db.collection('doctor').where(
                    'city', '==', city).where(
                    'surname', '>=', surname).where(
                    'surname', '<=', end_surname).limit(10)

            else:
                query = db.collection('doctor').where(
                    'city', '==', city).where(
                    'suburb', '==', suburb).where(
                    'surname', '>=', surname).where(
                    'surname', '<=', end_surname).limit(20)

            docs = query.get()

            doctors = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict.update({'id': doc.id})
                doctors.append(doc_dict)

            # TODO Implement pagination
            return render(request, 'access_admin/search_doctor.html', {
                'form': form,
                'doctors': doctors
            })
    else:
        form = DoctorSearchForm(cities_list=cities_list)

    context = {
        'form': form
    }
    return render(request, 'access_admin/search_doctor.html', context)


def view_doctor(request, doctor_id):

    doc_ref = db.collection('doctor').document(doctor_id)
    doc = doc_ref.get().to_dict()
    print(doc)

    # Avoid division by zero
    if doc['lastMonthPremium'] == 0:
        premium_change = 0
    else:
        premium_change = (doc['thisMonthPremium'] / doc['lastMonthPremium'])-1

    if doc['previousPaidMembers'] == 0:
        member_change = 0
    else:
        member_change = (doc['currentPaidMembers'] / doc['previousPaidMembers']) - 1

    if doc['previousNewMembers'] == 0:
        new_member_change = 0
    else:
        new_member_change = (doc['currentNewMembers'] / doc['previousNewMembers']) - 1

    unpaid_premium = doc['totalPossiblePremium'] - doc['thisMonthPremium']
    unpaid_members = doc['totalMembers'] - doc['currentPaidMembers']

    context = {
        'doctor_id': doctor_id,
        'doc': doc,
        'member_change': member_change,
        'new_member_change': new_member_change,
        'premium_change': premium_change,
        'unpaid_members': unpaid_members,
        'unpaid_premium': unpaid_premium
    }

    return render(request, 'access_admin/view_doctor.html', context)


def doctor_search_policy(request):

    if request.method == 'POST':
        form = PolicySearchForm(request.POST)
        if form.is_valid():
            policy_number = form.cleaned_data['policy_number']
            surname = form.cleaned_data['surname']
            id_number = form.cleaned_data['id_number']
            print(policy_number)
            print(surname)
            print(id_number)

            return render(request, 'access_admin/doctor_search_policy.html', {
                'form': form,
            })

    else:
        form = PolicySearchForm()

    return render(request, 'access_admin/doctor_search_policy.html', {
        'form': form
    })


def add_specialist(request):

    # Get list of cities from database
    cities = db.collection('cities').document('cities').get().to_dict()['cities']

    # convert list to tuple of tuples
    cities_list = tuple((city, city) for city in cities)

    if request.method == 'POST':
        form = SpecialistForm(request.POST, cities_list=cities_list)
        if form.is_valid():

            title = form.cleaned_data["title"]
            first_name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["surname"]
            phone2 = form.cleaned_data['phone2']
            phone1 = form.cleaned_data['phone1']

            combined_name = f'{title} {first_name[0]}. {surname}'

            if phone2 == '':
                phones = [phone1,]
            else:
                phones = [phone1, phone2]

            data = {
                'firstName': first_name,
                'surname': surname.upper(),
                'title': title,
                'name': combined_name,
                'gender': form.cleaned_data['gender'],
                'address': form.cleaned_data['address'],
                'city': form.cleaned_data['city'],
                'phone': phones,
                'email': form.cleaned_data['email'],
                'specialty': form.cleaned_data['specialty']
            }

            print(data)

            doc_ref = db.collection('specialist').document()
            doc_ref.set(data)

            return redirect('access_admin:index')  # TODO consider redirecting to doctor view if request
    else:
        form = SpecialistForm(cities_list=cities_list)

    return render(request, 'access_admin/add_specialist.html', {'specialist_form': form})


def view_specialist(request, specialist_id):

    doc_ref = db.collection('specialist').document(specialist_id)
    doc = doc_ref.get().to_dict()
    print(doc)

    # Avoid division by zero
    if doc['lastMonthPremium'] == 0:
        premium_change = 0
    else:
        premium_change = (doc['thisMonthPremium'] / doc['lastMonthPremium']) - 1

    if doc['previousPaidMembers'] == 0:
        member_change = 0
    else:
        member_change = (doc['currentPaidMembers'] / doc['previousPaidMembers']) - 1

    if doc['previousNewMembers'] == 0:
        new_member_change = 0
    else:
        new_member_change = (doc['currentNewMembers'] / doc['previousNewMembers']) - 1

    unpaid_premium = doc['totalPossiblePremium'] - doc['thisMonthPremium']
    unpaid_members = doc['totalMembers'] - doc['currentPaidMembers']

    context = {
        'doctor_id': specialist_id,
        'doc': doc,
        'easy_specialty': SPECIALTIES_DICT[doc['specialty']],
        'member_change': member_change,
        'new_member_change': new_member_change,
        'premium_change': premium_change,
        'unpaid_members': unpaid_members,
        'unpaid_premium': unpaid_premium
    }
    return render(request, 'access_admin/view_specialist.html', context)


def search_specialist(request, doctor_id=''):
    # TODO: Implement 'next' navigation
    specialty = request.GET.get('s', False)
    print(specialty)

    if doctor_id != '':
        doctor_ref = db.collection('doctor').document(doctor_id)
        doc = doctor_ref.get().to_dict()
        doctor_details = doc
        specialties = tuple()

        if doc['physician']:
            pass
        else:
            specialties += (('physician', 'Physician'),)

        if doc['generalSurgeon']:
            pass
        else:
            specialties += (('generalSurgeon', 'General surgeon'),)

        if doc['obsAndGynae']:
            pass
        else:
            specialties += (('obsAndGynae', 'Obstetrician and gynaecologist'),)

        if doc['ophthalmologist']:
            pass
        else:
            specialties += (('ophthalmologist', 'Ophthalmologist'),)

        if doc['orthopaedicSurgeon']:
            pass
        else:
            specialties += (('orthopaedicSurgeon', 'Orthopaedic Surgeon'),)

        if doc['physiotherapist']:
            pass
        else:
            specialties += (('physiotherapist', 'Physiotherapist'),)

        if doc['eNT']:
            pass
        else:
            specialties += (('eNT', 'Ear, nose and throat '),)

        if bool(doc['paediatrician']):
            pass
        else:
            specialties += (('paediatrician', 'Paediatrician'),)

    else:
        doctor_details = False
        specialties = SPECIALTIES

    cities = db.collection('cities').document('cities').get().to_dict()['cities']

    # convert list to tuple of tuples
    cities_list = tuple((city, city) for city in cities)

    if request.method == 'POST':

        form = SpecialistSearchForm(
            request.POST,
            cities_list=cities_list,
            specialties_list=specialties
        )
        print(form)

        if form.is_valid():

            city = form.cleaned_data['city']
            specialty = form.cleaned_data['specialty']
            surname = form.cleaned_data['surname'].upper()
            end_surname = surname + 'z'

            if city == '':
                query = db.collection('specialist').where(
                    'specialty', '==', specialty).where(
                    'surname', '>=', surname).where(
                    'surname', '<=', end_surname).limit(10)

            else:
                query = db.collection('specialist').where(
                    'city', '==', city).where(
                    'specialty', '==', specialty).where(
                    'surname', '>=', surname).where(
                    'surname', '<=', end_surname).limit(20)

            docs = query.get()
            specialists = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict.update({'id': doc.id})
                specialists.append(doc_dict)

            for doc in specialists:
                doc.update({'f_specialty': SPECIALTIES_DICT[doc['specialty']]})

            print(specialists)
            return render(request, 'access_admin/search_specialist.html',
                          {
                              'form': form,
                              'specialists': specialists,
                              'doctor_id': doctor_id,
                              'doctor': doctor_details
                          })

    else:
        if specialty:
            form = SpecialistSearchForm(
                {
                    'specialty': specialty,
                },
                cities_list=cities_list,
                specialties_list=specialties,
            )
        else:
            form = SpecialistSearchForm(
                cities_list=cities_list,
                specialties_list=specialties,
            )

    return render(request, 'access_admin/search_specialist.html', {
        'form': form,
        'doctor_id': doctor_id,
        'doctor': doctor_details
    })


def specialist_doctor(request, doctor_id, specialist_id):

    # TODO Error catching (where records cannot be located in system
    # TODO Implement messaging toasts

    doc_ref = db.collection('doctor').document(doctor_id)
    doctor = doc_ref.get().to_dict()

    spec_ref = db.collection('specialist').document(specialist_id)
    specialist = spec_ref.get().to_dict()

    doc_ref.update({
        specialist['specialty']: {
            'id': specialist_id,
            'name': specialist['name'],
            'premium': 0
        },
        'specialists': firestore.ArrayUnion([specialist_id])
    })

    spec_ref.update({u'doctors': firestore.ArrayUnion([{
        'id': doctor_id,
        'name': doctor['name'],
        'paidMembers': 0,
        'premium': 0,
        'totalMembers': 0
    }])})

    return redirect('access_admin:view_doctor', doctor_id)


def search_policy(request, last=False):

    last = False

    if request.method == 'POST':

        form = PolicySearchForm(request.POST)

        # check if user has pressed the 'next' button
        if 'next' in request.POST:
            # get the ID of the last policy in current batch
            last = request.POST['last']

        if form.is_valid():
            policy_number = form.cleaned_data['policy_number']
            surname = form.cleaned_data['surname']
            id_number = form.cleaned_data['id_number']

            per_page = 10
            # query = db.collection('policy')
            # policy_docs = query.get()

            if last: # request is coming from next button with, a last policy from the batch
                policy_docs = policy_query(
                    id_number=id_number,
                    surname=surname,
                    per_page=per_page,
                    start_after=last
                )
            else:
                policy_docs = policy_query(
                    id_number=id_number,
                    surname=surname,
                    per_page=per_page,
                )

            policies = []
            for pol in policy_docs:
                pol_dict = pol.to_dict()

                monthly_premium = pol_dict['basicPremium'] + pol_dict['chronicAddOn']
                pol_dict.update({
                    'id': pol.id,
                    'monthly_premium': monthly_premium
                })
                policies.append(pol_dict)

            # check if there's still more documents in the database
            if len(policies) == per_page:
                last_doc = policies[len(policies)-1]
                last = last_doc['id']

            else:
                # no more documents, disable the next button
                last = False

            print(policies)

            return render(request, 'access_admin/search_policy.html', {
                'form': form,
                'policies': policies,
                'last': last
            })

    else:
        form = PolicySearchForm()

    return render(request, 'access_admin/search_policy.html', {
        'form': form,
        'last': last
    })


def policy_query(
        id_number,
        policy_number=False,
        surname='',
        per_page=10,
        start_after=False,
        status='active'
):
    end_surname = surname + 'z'

    if id_number == '':
        if start_after:
            doc = db.collection('policy').document(start_after).get()

            q = db.collection('policy').where(
                'surname', '>=', surname).where(
                'surname', '<=', end_surname).where(
                'status', '==', status).order_by(
                'surname').limit(per_page).start_after(doc)
        else:
            q = db.collection('policy').where(
                'surname', '>=', surname).where(
                'surname', '<=', end_surname).where(
                'status', '==', status).order_by(
                'surname').limit(per_page)
    else:
        if start_after:
            doc = db.collection('policy').document(start_after).get()

            q = db.collection('policy').where(
                'surname', '>=', surname).where(
                'surname', '<=', end_surname).where(
                'idNumber', '==', id_number).where(
                'status', '==', status).order_by(
                'surname').limit(per_page).start_after(doc)
        else:
            q = db.collection('policy').where(
                'surname', '>=', surname).where(
                'surname', '<=', end_surname).where(
                'idNumber', '==', id_number).where(
                'status', '==', status).order_by(
                'surname').limit(per_page)

    return q.get()


def view_policy(request, policy_id):
    policy_ref = db.collection('policy').document(policy_id)
    policy_doc = policy_ref.get()
    policy = policy_doc.to_dict()
    policy.update({'id': policy_doc.id})

    receipt_query = db.collection('receipts').where(
        'policyID', '==', policy_id).order_by('datePaid', direction=firestore.Query.DESCENDING).limit(5)

    receipts = [receipt.to_dict() for receipt in receipt_query.get()]

    if len(receipts) == 0:
        receipts = False

    return render(request, 'access_admin/view_policy.html', {
        'policy': policy,
        'receipts': receipts
    })

# Todo
# - Implement capture deductions (from admin side)
# - view deduction (doctor can access by menu and by clicking deductions summary on dashboard)


