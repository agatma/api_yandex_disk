from django.db import models

FILE = "FILE"
FOLDER = "FOLDER"
TYPE = [
    (FILE, "FILE"),
    (FOLDER, "FOLDER"),
]


class Item(models.Model):
    """Модель для работы с элементом"""

    id = models.UUIDField(
        "ID элемента",
        primary_key=True,
        unique=True,
        null=False,
    )

    url = models.CharField("Ссылка на файл", max_length=255, null=True, blank=True)

    date = models.DateTimeField("Дата обновления", db_index=True)
    parentId = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="Родитель элемента",
        blank=True,
        null=True,
    )
    type = models.CharField("Тип файла", max_length=6, choices=TYPE)
    size = models.IntegerField("Размер файла", blank=True, null=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.id}"
