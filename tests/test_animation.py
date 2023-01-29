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
def test_animation_model_stateIn_move():
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
	obj.type = ObjectType.RECTANGLE
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
	ani.scale = 1.0  # not used by MOVE
	ani.save()

	state = obj.stateIn(0, 7)

	assert state.x == 36.66666666666667
	assert state.y == 10
	assert state.width == 80
	assert state.height == 50
	assert state.active


@pytest.mark.django_db
def test_animation_model_stateIn_scale():
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
	obj.type = ObjectType.RECTANGLE
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
	ani.type = AnimationType.SCALE
	ani.start = 2
	ani.end = 5
	ani.dx = 0  # not used by SCALE
	ani.dy = 0  # not used by SCALE
	ani.scale = 2.0
	ani.save()

	state = obj.stateIn(0, 7)

	assert state.x == -258.64197530864186
	assert state.y == -142.90123456790116
	assert state.width == 617.2839506172837
	assert state.height == 385.8024691358023
	assert state.active
