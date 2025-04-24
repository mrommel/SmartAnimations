from django.contrib import admin

from scenes.admin_forms import SceneAdmin
from scenes.models import Scene, SceneCamera, SceneObject

admin.site.register(Scene, SceneAdmin)
admin.site.register(SceneCamera)
admin.site.register(SceneObject)
