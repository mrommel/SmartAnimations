import pytest

from animations.models import AnimationModel, ObjectModel, ObjectType, ObjectAnimationModel, AnimationType


@pytest.mark.django_db
def test_animation_creation():
	new_animation = AnimationModel()
	new_animation.name = 'dummy'
	new_animation.width = 100
	new_animation.height = 100
	new_animation.start = 0
	new_animation.end = 10
	new_animation.save()

	animation = AnimationModel.objects.get(name='dummy')
	assert animation.name == 'dummy'
	assert animation.width == 100
	assert animation.height == 100
	assert animation.start == 0
	assert animation.end == 10


@pytest.mark.django_db
def test_animation_model():
	new_animation = AnimationModel()
	new_animation.name = 'dummy'
	new_animation.width = 100
	new_animation.height = 100
	new_animation.start = 0
	new_animation.end = 10
	new_animation.save()

	obj = ObjectModel()
	obj.name = 'base object'
	obj.animation = new_animation
	obj.type = ObjectType.UNKNOWN
	obj.zindex = 1
	obj.image = None
	obj.x_coord = 10
	obj.y_coord = 10
	obj.width = 80
	obj.height = 50
	obj.color = '#FFFFFF'
	obj.save()

	ani = ObjectAnimationModel()
	ani.object = obj
	ani.type = AnimationType.MOVE
	ani.start = 2
	ani.end = 5
	ani.dx = 20
	ani.dy = 0
	ani.scale = 1.0
	ani.save()

	state = obj.stateIn(0, 7)

	assert state.x == 36.66666666666667
	assert state.y == 10
	assert state.width == 80
	assert state.height == 50
