from django.urls import path
from .views import ManageHousesView

urlpatterns = [
    path('manage', ManageHousesView.as_view()),
]
