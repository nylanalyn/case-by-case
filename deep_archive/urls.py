from django.contrib import admin
from django.urls import include, path

from towns.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("boards/", include("boards.urls")),
    path("town/", include("towns.urls")),
    path("cases/", include("cases.urls")),
]
