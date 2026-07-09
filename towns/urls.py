from django.urls import path

from . import views

urlpatterns = [
    path("", views.town_home, name="town_home"),
    path("locations/<slug:slug>/", views.location_detail, name="location_detail"),
]
