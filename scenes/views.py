from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.renderers import BaseRenderer
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.views.decorators.clickjacking import xframe_options_exempt

from scenes.forms import SceneForm, SceneCameraForm
from scenes.models import Scene, SceneCamera


def is_admin(user):
    return user.is_superuser


admin_required = user_passes_test(lambda user: user.is_superuser)


def dashboard(request):
    template: BaseRenderer = loader.get_template("scenes/dashboard.html")
    context = {
        "title": "Dashboard",
    }
    return HttpResponse(template.render(context, request))


def list_scenes(request):
    scenes = Scene.objects.all()

    template: BaseRenderer = loader.get_template("scenes/list_scenes.html")
    context = {
        "title": "Scenes",
        "num_scenes": len(scenes),
        "scenes": scenes,
    }
    return HttpResponse(template.render(context, request))


@login_required
@admin_required
def add_scene(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        name = request.POST.get("name")

        scene = Scene(name=name)
        scene.save()

        # Redirect to the task list page
        return redirect("list_scenes")
    else:
        form = SceneForm()

        template: BaseRenderer = loader.get_template("scenes/add_scene.html")
        context = {
            "title": "Add Scene",
            "form": form,
        }
        return HttpResponse(template.render(context, request))


def detail_scene(request, scene_id: str):
    scene = get_object_or_404(Scene, pk=scene_id)

    if request.method == "POST":
        scene_camera_form = SceneCameraForm(request.POST)
        if scene_camera_form.is_valid():
            # try to find existing camera scene
            camera_scene = SceneCamera.objects.filter(scene=scene).first()
            if camera_scene is None:
                print('Create new SceneCamera')
                camera_scene = SceneCamera()

            camera_scene.camera_type = scene_camera_form.cleaned_data['camera_type']
            camera_scene.position_x = scene_camera_form.cleaned_data['position_x']
            camera_scene.position_y = scene_camera_form.cleaned_data['position_y']
            camera_scene.position_z = scene_camera_form.cleaned_data['position_z']
            camera_scene.fov = scene_camera_form.cleaned_data['fov']
            camera_scene.near = scene_camera_form.cleaned_data['near']
            camera_scene.far = scene_camera_form.cleaned_data['far']

            camera_scene.save()

            return JsonResponse({"success": True})
        else:
            print(f"Form is not valid: {scene_camera_form.errors}")
            return JsonResponse({"success": False, "errors": scene_camera_form.errors})
    else:
        camera_scene = SceneCamera.objects.filter(scene=scene).first()
        if camera_scene is None:
            scene_camera_form = SceneCameraForm(instance=camera_scene)
        else:
            scene_camera_form = SceneCameraForm()
            scene_camera_form.scene = scene

        template: BaseRenderer = loader.get_template("scenes/detail.html")
        context = {
            "title": f"Scene {scene.name}",
            "scene": scene,
            "scene_camera_form": scene_camera_form,
        }
        return HttpResponse(template.render(context, request))


@xframe_options_exempt
def detail_iframe(request, scene_id: str):
    scene = get_object_or_404(Scene, pk=scene_id)

    template: BaseRenderer = loader.get_template("scenes/detail_iframe.html")
    context = {
        "title": f"Scene {scene.name}",
        "scene": scene,
    }
    return HttpResponse(template.render(context, request))
