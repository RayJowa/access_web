from django.urls import path

from . import views

app_name = 'access_admin'



urlpatterns = [
    path('', views.index, name='index'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('add_specialist', views.add_specialist, name='add_specialist'),
    path('doctor/<str:doctor_id>/', views.view_doctor, name='view_doctor'),
    path('fetch_suburbs', views.fetch_suburbs, name='fetch_suburbs'),
    path('register', views.register, name='register'),
    path('search_specialist', views.search_specialist, name='search_specialist'),
    path('search_specialist/<str:doctor_id>/', views.search_specialist, name='doc_search_specialist'),
    path('signin', views.sign_in, {'next_to': 'next'}, name='sign_in'),
    path('signout', views.sign_out, name='sign_out'),
    path('specialist_doctor/<str:doctor_id>/<str:specialist_id>/', views.specialist_doctor, name='specialist_doctor'),
]
