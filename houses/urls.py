from django.urls import path
from .views import ManageHousesView, HouseDetailView

urlpatterns = [
    path('manage', ManageHousesView.as_view()),
    path('detail', HouseDetailView.as_view()),
]
