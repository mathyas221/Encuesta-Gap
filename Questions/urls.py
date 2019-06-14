from django.urls import path
from Questions import views


urlpatterns = [
    path('login/', views.auth_login, name="login"),
    path('logout/', views.auth_logout, name="logout"),
    path('question/', views.question, name='question'),
    path('getanswer/', views.getanswer, name='getanswer'),
    path('createpersonal/', views.createpersonal, name='createpersonal'),
]