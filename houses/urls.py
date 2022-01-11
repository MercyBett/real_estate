from django.urls import path
from .views import HousesView, ManageHousesView, HouseDetailView,  SearchHouseView

urlpatterns = [
    path('manage', ManageHousesView.as_view()),
    path('detail', HouseDetailView.as_view()),
    path('get-houses', HousesView.as_view()),
    path('search', SearchHouseView.as_view()),
]
