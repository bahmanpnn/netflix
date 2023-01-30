from django.urls import path
from .views import *

urlpatterns = [
    path('sign_up', Home.as_view())
]
