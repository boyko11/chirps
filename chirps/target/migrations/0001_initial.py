# Generated by Django 4.2.2 on 2023-07-07 18:00

import django.db.models.deletion
import fernet_fields.fields
from django.conf import settings
from django.db import migrations, models

import target.custom_fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTarget',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=128)),
                (
                    'polymorphic_ctype',
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='polymorphic_%(app_label)s.%(class)s_set+',
                        to='contenttypes.contenttype',
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='MantiumTarget',
            fields=[
                (
                    'basetarget_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='target.basetarget',
                    ),
                ),
                ('app_id', models.CharField(max_length=256)),
                ('client_id', models.CharField(max_length=256)),
                (
                    'client_secret',
                    fernet_fields.fields.EncryptedCharField(max_length=256),
                ),
                ('top_k', models.IntegerField(default=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('target.basetarget',),
        ),
        migrations.CreateModel(
            name='PineconeTarget',
            fields=[
                (
                    'basetarget_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='target.basetarget',
                    ),
                ),
                (
                    'api_key',
                    target.custom_fields.CustomEncryptedCharField(max_length=256),
                ),
                (
                    'environment',
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ('index_name', models.CharField(blank=True, max_length=256, null=True)),
                (
                    'project_name',
                    models.CharField(blank=True, max_length=256, null=True),
                ),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('target.basetarget',),
        ),
        migrations.CreateModel(
            name='RedisTarget',
            fields=[
                (
                    'basetarget_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='target.basetarget',
                    ),
                ),
                ('host', models.CharField(max_length=1048)),
                ('port', models.IntegerField()),
                ('database_name', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(blank=True, max_length=2048, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('target.basetarget',),
        ),
    ]
