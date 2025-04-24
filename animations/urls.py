from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="home", permanent=True), name="index"),
    path("home", views.index, name="index"),
    path("animation/<str:animation_id>/", views.animation, name="animation"),
    path(
        "render/<str:animation_id>/<int:frame_id>",
        views.render_animation,
        name="animation",
    ),
    # admin actions
    path(
        "export/<str:animation_id>/gif",
        views.export_animation_gif,
        name="export_animation_gif",
    ),
    # test
    path("test3d", views.test3d, name="test3d"),
]
