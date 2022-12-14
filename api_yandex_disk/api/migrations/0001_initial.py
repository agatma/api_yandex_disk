# Generated by Django 2.2.16 on 2022-09-16 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID элемента",
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Ссылка на файл",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(db_index=True, verbose_name="Дата обновления"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("FILE", "FILE"), ("FOLDER", "FOLDER")],
                        max_length=6,
                        verbose_name="Тип файла",
                    ),
                ),
                (
                    "size",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Размер файла"
                    ),
                ),
                (
                    "parentId",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="api.Item",
                        verbose_name="Родитель элемента",
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
            },
        ),
    ]
