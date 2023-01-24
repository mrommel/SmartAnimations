from colorfield.fields import ColorField
from django.db.models import CheckConstraint, Q, Model, IntegerField, CharField, TextChoices, ForeignKey, CASCADE, \
	ImageField, FloatField
from django.utils.translation import gettext_lazy as _


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

	def __str__(self):
		return self.name


class ObjectType(TextChoices):
	UNKNOWN = 'UN', _('Unknown')
	IMAGE = 'IM', _('Image')
	RECTANGLE = 'RE', _('Rectangle')


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

	class Meta:
		constraints = [
			CheckConstraint(
				check=Q(type__in=AnimationType.values),
				name="valid_animation_type")
		]

	def __str__(self):
		return f'{self.type_name()} animation of {self.object.name}'
