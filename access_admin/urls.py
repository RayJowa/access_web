from django.urls import path

from . import views

app_name = 'access_admin'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('register', views.register, name='register'),
    path('signin', views.sign_in, {'next_to': 'next'}, name='sign_in'),
    path('signout', views.sign_out, name='sign_out'),
]
