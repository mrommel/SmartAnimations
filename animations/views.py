from PIL import ImageDraw, Image
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from animations.forms import NewAnimationForm
from animations.models import AnimationModel, ObjectModel, ObjectAnimationModel, ObjectType
from smartanimations.settings import BASE_DIR


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

	img = Image.new('RGBA', (animation_model.width, animation_model.height), (255, 0, 0, 0))

	draw = ImageDraw.Draw(img)

	for obj in ObjectModel.objects.filter(animation=animation_model):
		state = obj.stateIn(animation_model.start, frame_id)
		if obj.type == ObjectType.RECTANGLE:
			draw.rectangle((state.x, state.y, state.x + state.width, state.y + state.height), outline='teal', fill=f'{obj.color}', width=0)
		elif obj.type == ObjectType.IMAGE:
			# print(f'base: {BASE_DIR}')
			# print(f'image: {obj.image}')
			image_path = obj.full_path()
			im2 = Image.open(image_path)
			size = (int(state.width), int(state.height))
			im2 = im2.resize(size, Image.Resampling.LANCZOS)
			area = (int(state.x), int(state.y))  # , state.x + state.width, state.y + state.height)
			img.paste(im2, area)
		else:
			raise AttributeError(f'unsupported type: {obj.type}')

	response = HttpResponse(content_type="image/png")
	img.save(response, "PNG")
	return response

