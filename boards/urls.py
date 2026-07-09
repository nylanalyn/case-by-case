from django.urls import path

from . import views

urlpatterns = [
    path("posts/<int:post_id>/delete/", views.delete_post, name="delete_board_post"),
]
