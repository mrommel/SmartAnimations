import pytest

from animations.models import AnimationModel


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
