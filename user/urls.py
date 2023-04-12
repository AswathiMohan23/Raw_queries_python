from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistration.as_view(), name="register"),
    path('update', views.UserRegistration.as_view(), name="update"),
    path('delete', views.UserRegistration.as_view(), name='delete'),

]
