from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm

from scenes.models import Scene, SceneCamera


class SceneForm(ModelForm):
    class Meta:
        model = Scene
        fields = [
            "name",
        ]


class SceneCameraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "properties-form"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_tag = False
        # self.helper.form_action = 'submit_survey'
        # self.helper.add_input(Submit('', 'Save'))

    class Meta:
        model = SceneCamera
        fields = [
            "camera_type",
            "position_x",
            "position_y",
            "position_z",
            "fov",
            "near",
            "far",
        ]
        exclude = ("scene",)
        widgets = {
            "fov": forms.TextInput(attrs={"placeholder": "focal length"}),
        }
