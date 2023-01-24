from django.contrib import admin

from animations.forms import AnimationModelAdmin
from animations.models import AnimationModel, ObjectModel, ObjectAnimationModel

# Register your models here.
admin.site.register(AnimationModel, AnimationModelAdmin)
admin.site.register(ObjectModel)
admin.site.register(ObjectAnimationModel)
