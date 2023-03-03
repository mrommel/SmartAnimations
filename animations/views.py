import io
import os
import uuid

import imageio
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from django.template import loader

from animations.forms import NewAnimationForm
from animations.models import AnimationModel


def index(request):
	# create a form instance and populate it with data from the request:
	new_animation_form = NewAnimationForm(request.POST or None)
	# check whether it's valid:
	if new_animation_form.is_valid():
		# process the data in form.cleaned_data as required
		new_animation_form.save()
		# redirect to a new URL:
		return HttpResponseRedirect('/animations/home?action=added')

	animations = AnimationModel.objects.order_by('-pk')[:10]

	template = loader.get_template('index.html')
	context = {
		'navi_home': 'active',
		'animations': animations,
		'form': new_animation_form,
	}
	return HttpResponse(template.render(context, request))


def animation(request, animation_id):
	try:
		animation_model = AnimationModel.objects.get(pk=animation_id)
	except AnimationModel.DoesNotExist:
		raise Http404("Animation does not exist")

	template = loader.get_template('animation.html')
	context = {
		'navi_home': 'active',
		'animation': animation_model,
	}
	return HttpResponse(template.render(context, request))


def render_animation(request, animation_id, frame_id):
	try:
		animation_model = AnimationModel.objects.get(pk=animation_id)
	except AnimationModel.DoesNotExist:
		raise Http404("Animation does not exist")

	if not animation_model.start <= frame_id <= animation_model.end:
		return HttpResponse(f'{frame_id} must be within [{animation_model.start}-{animation_model.end}]', status=400)

	img = animation_model.frame_image(frame_id)

	response = HttpResponse(content_type="image/png")
	img.save(response, "PNG")
	return response


def export_animation_gif(request, animation_id):
	try:
		animation_model = AnimationModel.objects.get(pk=animation_id)
	except AnimationModel.DoesNotExist:
		raise Http404("Animation does not exist")

	images = []

	for frame_id in range(animation_model.start, animation_model.end):
		img = animation_model.frame_image(frame_id)
		images.append(img)

	buffer = io.BytesIO()
	imageio.mimwrite(buffer, images)

	tmp_out = f'out-{uuid.UUID}.gif'

	# output
	buffer.seek(0)
	imageio.mimwrite(tmp_out, images)

	img = open(tmp_out, 'rb')
	response = FileResponse(img, content_type="image/gif")

	# cleanup
	os.remove(tmp_out)

	return response


def test3d(request):
	template = loader.get_template('test3d.html')
	context = {
		'navi_home': 'active',
	}
	return HttpResponse(template.render(context, request))
