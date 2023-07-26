# Generated by Django 4.2.3 on 2023-07-25 15:20

import django.db.models.deletion
import fernet_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('asset', '0001_initial'),
        ('policy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scan',
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
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('description', models.TextField()),
                ('celery_task_id', models.CharField(max_length=256, null=True)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('Queued', 'Queued'),
                            ('Running', 'Running'),
                            ('Complete', 'Complete'),
                            ('Failed', 'Failed'),
                        ],
                        default='Queued',
                        max_length=32,
                    ),
                ),
                ('policies', models.ManyToManyField(to='policy.policy')),
                (
                    'user',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ScanAsset',
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
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('celery_task_id', models.CharField(max_length=256, null=True)),
                ('progress', models.IntegerField(default=0)),
                (
                    'scan',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='scan_assets',
                        to='scan.scan',
                    ),
                ),
                (
                    'asset',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='asset.baseasset',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Result',
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
                ('text', fernet_fields.fields.EncryptedTextField()),
                (
                    'rule',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='policy.rule'),
                ),
                (
                    'scan_asset',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='results',
                        to='scan.scanasset',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Finding',
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
                ('offset', models.IntegerField()),
                ('length', models.IntegerField()),
                (
                    'result',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='findings',
                        to='scan.result',
                    ),
                ),
            ],
        ),
    ]
