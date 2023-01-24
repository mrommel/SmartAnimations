import PIL
from PIL import ImageDraw
from django.http import HttpResponse, Http404, HttpResponseRedirect
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

	img = PIL.Image.new('RGBA', (animation_model.width, animation_model.height), (255, 0, 0, 0))

	draw = ImageDraw.Draw(img)
	draw.rectangle((100, 100, 300, 300), outline='teal', fill='orange', width=25)

	response = HttpResponse(content_type="image/png")
	img.save(response, "PNG")
	return response

