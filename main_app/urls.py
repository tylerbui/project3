from django.urls import path, include
from . import views
from .views import PostCreate, ProfileUpdate, profile, PostDelete, PostDetailView

urlpatterns = [
    path('',views.home, name='home'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:pk>/profile_update/',views.ProfileUpdate.as_view(), name='profile_update'),
    path('main_app/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_confirm_delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
