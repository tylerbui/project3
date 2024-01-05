from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('main_app/create/', views.PostCreate.as_view(), name='post_create'),
]
