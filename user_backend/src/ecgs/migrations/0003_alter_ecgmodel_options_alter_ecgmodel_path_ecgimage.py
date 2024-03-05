# Generated by Django 4.2.11 on 2024-03-05 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ecgs", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ecgmodel",
            options={"verbose_name": "ЭКГ", "verbose_name_plural": "ЭКГ"},
        ),
        migrations.AlterField(
            model_name="ecgmodel",
            name="path",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.CreateModel(
            name="EcgImage",
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
                ("image", models.ImageField(upload_to="")),
                (
                    "ecg",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="ecgs.ecgmodel",
                    ),
                ),
            ],
        ),
    ]
