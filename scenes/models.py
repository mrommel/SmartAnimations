from typing import Optional

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Model
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy
from django_enumfield import enum


class Scene(Model):
    name = models.CharField(
        max_length=100,
        help_text="Enter a name of the Scene",
    )

    objects = models.Manager()

    def camera_properties(self):  # -> Optional[SceneCamera]:
        return SceneCamera.objects.filter(scene=self).first()

    def __str__(self):
        return self.name


class CameraType(enum.Enum):
    DEFAULT = 0
    TOP = 1

    CUSTOM = 12  # x, y, z can be set by user

    __labels__ = {
        DEFAULT: gettext_lazy("Default"),
        TOP: gettext_lazy("Top"),
        CUSTOM: gettext_lazy("Custom"),
    }

    def position(self) -> (Optional[float], Optional[float], Optional[float]):
        if self == CameraType.DEFAULT:
            return 0, 50, 500
        elif self == CameraType.TOP:
            return 0, 0, 100

        return None, None, None

    def perspective(self):  # fov, (aspect), near, far
        if self == CameraType.DEFAULT:
            return (
                50,
                0.1,
                2000,
            )  # 50, window.innerWidth / window.innerHeight, 0.01, 10000

        if self == CameraType.TOP:
            return 50, 0.1, 2000

        return None, None, None


class SceneCamera(Model):
    scene = models.OneToOneField(Scene, on_delete=models.CASCADE)
    camera_type = enum.EnumField(CameraType, default=CameraType.DEFAULT)
    position_x = models.FloatField()
    position_y = models.FloatField()
    position_z = models.FloatField()
    fov = models.FloatField()
    near = models.FloatField()
    far = models.FloatField()

    objects = models.Manager()

    def admin_link(self):
        return mark_safe(f'<a href="/admin/scenes/scenecamera/{self.id}/change/">Camera</a>')

    def __str__(self):
        return f"scene camera for {self.scene}"


class SceneObjectType(enum.Enum):
    PLANE = 0
    BILLBOARD = 0


class SceneObject(Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, )
    name = models.CharField(max_length=100, help_text="Enter a name of the Object", )
    object_type = enum.EnumField(SceneObjectType, default=SceneObjectType.PLANE)
    position_x = models.FloatField(default=0.0)
    position_y = models.FloatField(default=0.0)
    position_z = models.FloatField(default=0.0)
    normal_x = models.FloatField(default=0.0)
    normal_y = models.FloatField(default=0.0)
    normal_z = models.FloatField(default=1.0)
    width = models.FloatField(default=1.0)
    height = models.FloatField(default=1.0)
    opacity = models.FloatField(default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],)
    image = models.ImageField(upload_to='objects/', default=None, )

    def __str__(self):
        return f'{self.name} in {self.scene.name}'
