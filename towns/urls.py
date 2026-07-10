from django.urls import path

from . import views

urlpatterns = [
    path("", views.town_home, name="town_home"),
    path("pass-time/", views.pass_time_view, name="pass_time"),
    path("history/", views.town_history, name="town_history"),
    path("newspaper/", views.newspaper, name="newspaper"),
    path("locations/<slug:slug>/", views.location_detail, name="location_detail"),
]
