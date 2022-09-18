from datetime import datetime
from collections import OrderedDict
from typing import Optional, List
from api.models import Item, FOLDER


def cut_date_to_format(date: str) -> str:
    return f"{date[:19]}.{date[19:22]}Z"


def update_parent_date(instance: Optional[Item], dt: datetime) -> None:
    while instance:
        instance.date = dt
        instance.save()
        instance = instance.parentId


def count_size_of_folder(
    items: Optional[OrderedDict], total: Optional[List] = None
) -> int:
    """Считаем полный размер папки."""
    if total is None:
        total = []
    if not items:
        return sum(total)
    for i in items:
        if i["size"] and i["type"] != FOLDER:
            total.append(i["size"])
        if isinstance(i, OrderedDict):
            count_size_of_folder(i["children"], total)
    return sum(total)
