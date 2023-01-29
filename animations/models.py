from PIL import ImageDraw, Image
from colorfield.fields import ColorField
from django.db.models import CheckConstraint, Q, Model, IntegerField, CharField, TextChoices, ForeignKey, CASCADE, \
	ImageField, FloatField
from django.utils.translation import gettext_lazy as _

from smartanimations.settings import BASE_DIR


class AnimationModel(Model):
	name = CharField(max_length=100, help_text="Enter a name of the animation", )
	width = IntegerField()
	height = IntegerField()
	start = IntegerField(default=0)
	end = IntegerField(default=1)

	def object_models(self):
		result_list = []
		for obj in ObjectModel.objects.filter(animation=self):
			result_list.append(obj)
		return result_list

	def valid(self):
		if self.end <= self.start:
			return False

		for obj in ObjectModel.objects.filter(animation=self):
			for ani in ObjectAnimationModel.objects.filter(object=obj):
				if ani.end <= ani.start:
					return False

		return True

	def timeline(self):
		return list(range(self.start, self.end + 1))

	def frame_image(self, frame_id):
		img = Image.new('RGBA', (self.width, self.height), (255, 0, 0, 0))

		draw = ImageDraw.Draw(img)

		for obj in ObjectModel.objects.filter(animation=self):
			state = obj.stateIn(self.start, frame_id)
			if obj.type == ObjectType.RECTANGLE:
				draw.rectangle(
					(state.x, state.y, state.x + state.width, state.y + state.height),
					outline='teal',
					fill=f'{obj.color}',
					width=0
				)
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

		return img

	def __str__(self):
		return self.name


class ObjectType(TextChoices):
	UNKNOWN = 'UN', _('Unknown')
	IMAGE = 'IM', _('Image')
	RECTANGLE = 'RE', _('Rectangle')


class ObjectState:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height


class ObjectModel(Model):
	name = CharField(max_length=100, help_text="Enter a name of the object", )
	animation = ForeignKey(AnimationModel, on_delete=CASCADE)
	type = CharField(
		max_length=2,
		choices=ObjectType.choices,
		default=ObjectType.UNKNOWN,
	)
	zindex = IntegerField(default=0)
	image = ImageField(upload_to='media/objects', blank=True, null=True)
	x_coord = IntegerField(blank=True, null=True)
	y_coord = IntegerField(blank=True, null=True)
	width = IntegerField(blank=True, null=True)
	height = IntegerField(blank=True, null=True)
	color = ColorField(default='#FFFFFF')

	def full_path(self):
		return f'{BASE_DIR}/animations/{self.image}'

	def stateIn(self, start, frame_id):
		state = ObjectState(self.x_coord, self.y_coord, self.width, self.height)
		canvas_width = self.animation.width
		canvas_height = self.animation.height

		for index in range(start, frame_id):
			for ani in ObjectAnimationModel.objects.filter(object=self):
				if ani.start <= index <= ani.end:
					if ani.type == AnimationType.MOVE:
						state.x += ani.deltaX()
						state.y += ani.deltaY()
					elif ani.type == AnimationType.SCALE:
						ds = 1.0 + ani.deltaScale()
						dw = state.width * ds
						dh = state.height * ds
						state.x = (canvas_width - dw) / 2
						state.y = (canvas_height - dh) / 2
						state.width = dw
						state.height = dh

		return state

	class Meta:
		constraints = [
			CheckConstraint(
				check=Q(type__in=ObjectType.values),
				name="valid_objcet_type")
		]

	def __str__(self):
		return self.name


class AnimationType(TextChoices):
	UNKNOWN = 'UN', _('Unknown')
	MOVE = 'MO', _('Move')
	SCALE = 'SC', _('Scale')


class ObjectAnimationModel(Model):
	object = ForeignKey(ObjectModel, on_delete=CASCADE)
	type = CharField(
		max_length=2,
		choices=AnimationType.choices,
		default=AnimationType.UNKNOWN,
	)
	start = IntegerField(default=0)
	end = IntegerField(default=1)
	dx = IntegerField(default=0)
	dy = IntegerField(default=0)
	scale = FloatField(default=1)

	def type_name(self):
		return AnimationType(self.type).label

	def deltaX(self) -> float:
		dt = self.end - self.start
		return self.dx / dt

	def deltaY(self) -> float:
		dt = self.end - self.start
		return self.dy / dt

	def deltaScale(self) -> float:
		dt = self.end - self.start
		return self.scale / dt

	class Meta:
		constraints = [
			CheckConstraint(
				check=Q(type__in=AnimationType.values),
				name="valid_animation_type")
		]

	def __str__(self):
		return f'{self.type_name()} animation of {self.object.name}'
