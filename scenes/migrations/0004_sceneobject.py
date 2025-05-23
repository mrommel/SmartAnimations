# Generated by Django 4.2.11 on 2024-05-16 09:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import scenes.models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0003_scenecamera'),
    ]

    operations = [
        migrations.CreateModel(
            name='SceneObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a name of the Object', max_length=100)),
                ('object_type', django_enumfield.db.fields.EnumField(default=0, enum=scenes.models.SceneObjectType)),
                ('position_x', models.FloatField(default=0.0)),
                ('position_y', models.FloatField(default=0.0)),
                ('position_z', models.FloatField(default=0.0)),
                ('normal_x', models.FloatField(default=0.0)),
                ('normal_y', models.FloatField(default=0.0)),
                ('normal_z', models.FloatField(default=1.0)),
                ('width', models.FloatField(default=1.0)),
                ('height', models.FloatField(default=1.0)),
                ('opacity', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('image', models.ImageField(default=None, upload_to='objects/')),
                ('scene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenes.scene')),
            ],
        ),
    ]
