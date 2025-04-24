from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Row
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from animations.models import AnimationModel


class AnimationModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "render_animation_link",
    )

    def render_animation_link(self, obj):
        return mark_safe('<a href="/animations/export/%s/gif">Export GIF</a>' % obj.id)

    render_animation_link.allow_tags = True


class NewAnimationForm(forms.ModelForm):
    class Meta:
        model = AnimationModel
        fields = "__all__"

    helper = FormHelper()
    helper.form_class = "form-group"
    helper.layout = Layout(
        Field("name", css_class="form-control"),
        Fieldset(
            _("Dimensions"),
            Row(
                Field("width", css_class="form-control col-xs-5"),
                Field("height", css_class="form-control col-xs-5"),
                css_class="",
            ),
        ),
        Field("start", css_class="form-control mb-3"),
        Field("end", css_class="form-control"),
    )
