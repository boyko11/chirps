# Generated by Django 4.2.3 on 2023-07-19 13:51

from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("policy", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Finding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("offset", models.IntegerField()),
                ("length", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", fernet_fields.fields.EncryptedTextField()),
            ],
        ),
        migrations.CreateModel(
            name="Scan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(null=True)),
                ("description", models.TextField()),
                ("celery_task_id", models.CharField(max_length=256, null=True)),
                ("progress", models.IntegerField(default=0)),
                (
                    "policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="policy.policy"
                    ),
                ),
            ],
        ),
    ]
