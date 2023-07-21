# Generated by Django 4.2.3 on 2023-07-21 18:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('scan', '0002_alter_finding_result_alter_result_scan_target_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='status',
            field=models.CharField(
                choices=[
                    ('QU', 'Queued'),
                    ('RU', 'Running'),
                    ('CO', 'Complete'),
                    ('FA', 'Failed'),
                ],
                default='QU',
                max_length=2,
            ),
        ),
    ]
