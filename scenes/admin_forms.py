from typing import Optional

from django.contrib import admin

from scenes.models import Scene, SceneCamera, SceneObject


class SceneObjectInline(admin.TabularInline):
	model = SceneObject
	fk_name = "scene"
	extra = 0


class SceneAdmin(admin.ModelAdmin):
	model = Scene

	search_fields = [
		'name'
	]
	list_display = [
		'name',
	]
	readonly_fields = [
		'camera_admin_link',
	]
	inlines = [
		SceneObjectInline
	]

	def camera_admin_link(self, obj):
		camera_properties: Optional[SceneCamera] = obj.camera_properties()

		if camera_properties is None:
			return 'No Camera'

		return camera_properties.admin_link()
