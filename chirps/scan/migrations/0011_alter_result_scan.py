# Generated by Django 4.2.2 on 2023-07-03 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scan", "0010_alter_result_scan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="scan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="scan.scan"
            ),
        ),
    ]
