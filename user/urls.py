from django.urls import path
from .views import RegisterView, RetrieveView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('retrieve', RetrieveView.as_view()),
]
