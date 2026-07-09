from django.urls import path

from . import views

urlpatterns = [
    path("", views.case_list, name="case_list"),
    path("<int:case_id>/", views.case_detail, name="case_detail"),
    path("<int:case_id>/advance/", views.advance_case_view, name="advance_case"),
    path("journal/", views.clue_journal, name="clue_journal"),
]
