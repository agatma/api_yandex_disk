from typing import List, Dict, OrderedDict

from django.db.models import ObjectDoesNotExist
from api.models import Item, FILE, FOLDER


def items_validation(items: List[Dict]) -> bool:
    unique_uuid = {}
    for item in items:
        uuid = item["id"]
        parent_uuid = item["parentId"]
        if not item_validation(uuid, parent_uuid, unique_uuid):
            return False
        unique_uuid[uuid] = item["type"]
    return True


def item_validation(pk: str, parent: str, unique: Dict) -> bool:
    if pk in unique or (parent and parent in unique and unique[parent] != FOLDER):
        return False
    elif parent and parent not in unique:
        try:
            item = Item.objects.get(pk=parent)
        except ObjectDoesNotExist:
            return False
        if item.type != FOLDER:
            return False
    return True


def type_validation(type_value: str, data: OrderedDict) -> bool:
    if type_value == FOLDER and (data["size"] is not None or data["url"] is not None):
        return False
    elif type_value == FILE and (
        (data["size"] is None or data["size"] <= 0)
        or (data["url"] is None or len(data["url"]) > 255)
    ):
        return False
    return True
