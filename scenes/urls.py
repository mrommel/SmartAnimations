from django.urls import path
from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"),
    path("list", views.list_scenes, name="list_scenes"),
    path("add", views.add_scene, name="add_scene"),
    path("detail/<str:scene_id>", views.detail_scene, name="detail_scene"),
    path("detail_iframe/<str:scene_id>", views.detail_iframe, name="detail_iframe"),
]
