from django.urls import path

from . import views

app_name = 'access_admin'



urlpatterns = [
    path('', views.index, name='index'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('add_specialist', views.add_specialist, name='add_specialist'),
    path('dashboard', views.boss_dashboard, name='boss_dashboard'),
    path('doctor/<str:doctor_id>/', views.view_doctor, name='view_doctor'),
    path('doctor_search_policy', views.doctor_search_policy, name='doctor_search_policy'),
    path('fetch_suburbs', views.fetch_suburbs, name='fetch_suburbs'),
    path('policy/<str:policy_id>/', views.view_policy, name='view_policy'),
    path('register', views.register, name='register'),
    path('search_doctor', views.search_doctor, name='search_doctor'),
    path('search_policy', views.search_policy, name='search_policy'),
    path('search_specialist', views.search_specialist, name='search_specialist'),
    path('search_specialist/<str:doctor_id>/', views.search_specialist, name='doc_search_specialist'),
    path('signin', views.sign_in, {'next_to': 'next'}, name='sign_in'),
    path('signout', views.sign_out, name='sign_out'),
    path('specialist/<str:specialist_id>/', views.view_specialist, name='view_specialist'),
    path('specialist_doctor/<str:doctor_id>/<str:specialist_id>/', views.specialist_doctor, name='specialist_doctor'),
]
