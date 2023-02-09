from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view()),
    path('profiles/', ProfileList.as_view(), name='profile-list'),
    path('profiles/create-profile', CreateProfile.as_view(), name='create-profile'),
    path('watching/<str:profile_id>/', MovieList.as_view(), name='movies_list'),
]
