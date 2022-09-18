from collections import OrderedDict
from typing import Optional, List
from rest_framework.generics import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Item, FOLDER, TYPE, FILE
from api.validation import type_validation
from api.utils import cut_date_to_format, update_parent_date, count_size_of_folder


class ItemExportSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных об элемента"""

    id = serializers.UUIDField(read_only=True)
    url = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    parentId = serializers.UUIDField(read_only=True)
    size = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(read_only=True, choices=TYPE)

    def to_representation(self, data: Item) -> OrderedDict:
        """Форматируем дату"""
        data = super(ItemExportSerializer, self).to_representation(data)
        data["date"]: str = cut_date_to_format(data["date"])
        return data

    class Meta:
        model = Item
        fields = ("id", "date", "url", "parentId", "type", "size")


class ItemImportSerializer(serializers.ModelSerializer):
    """Сериализатор для импорта элемента"""

    id = serializers.UUIDField(allow_null=False)
    url = serializers.CharField(
        allow_null=True, allow_blank=True, default=None, max_length=255
    )
    date = serializers.DateTimeField(required=False)
    parentId = serializers.UUIDField(allow_null=True)
    size = serializers.IntegerField(allow_null=True, default=None)
    type = serializers.ChoiceField(choices=TYPE)

    def create(self, validated_data: dict) -> None:
        if validated_data["parentId"]:
            validated_data["parentId"] = get_object_or_404(
                Item, pk=validated_data["parentId"]
            )
        update_parent_date(validated_data["parentId"], validated_data["date"])
        return (
            self.update(Item.objects.get(pk=validated_data["id"]), validated_data)
            if Item.objects.filter(pk=validated_data["id"]).exists()
            else Item.objects.create(**validated_data)
        )

    def validate(self, data: OrderedDict) -> Optional[OrderedDict]:
        if not type_validation(data["type"], data):
            raise ValidationError()
        return data

    def update(self, instance, validated_data):
        """При обновлении элемента дополнительно меняем дату обновления"""
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        update_parent_date(validated_data["parentId"], validated_data["date"])
        instance.save()
        return instance

    def to_representation(self, data: Item) -> OrderedDict:
        """Форматируем дату"""
        data = super(ItemImportSerializer, self).to_representation(data)
        data["date"]: str = cut_date_to_format(data["date"])
        return data

    class Meta:
        fields = ("id", "date", "url", "parentId", "type", "size")
        model = Item


class ItemStructureExportSerializer(serializers.ModelSerializer):
    """Сериализатор для экспорта элемента и зависимостей"""

    id = serializers.UUIDField(read_only=True)
    url = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    parentId = serializers.UUIDField(read_only=True)
    size = serializers.IntegerField(read_only=True, default=0)
    type = serializers.ChoiceField(read_only=True, choices=TYPE)

    def to_representation(self, data: Item) -> OrderedDict:
        data = super(ItemStructureExportSerializer, self).to_representation(data)
        if not data["children"]:
            data["children"] = None if data["type"] == FILE else []
        if data["type"] == FOLDER:
            data["size"] = count_size_of_folder(data["children"])
        data["date"] = cut_date_to_format(data["date"])
        return data

    def get_fields(self):
        fields = super(ItemStructureExportSerializer, self).get_fields()
        fields["children"] = ItemStructureExportSerializer(many=True)
        return fields

    class Meta:
        model = Item
        fields = ("id", "date", "url", "parentId", "type", "size", "children")


class ItemHistoryExportSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения истории обновления элемента"""

    id = serializers.UUIDField(read_only=True)
    url = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    parentId = serializers.UUIDField(read_only=True)
    size = serializers.IntegerField(read_only=True, default=0)
    type = serializers.ChoiceField(read_only=True, choices=TYPE)

    def to_representation(self, data: Item) -> OrderedDict:
        data = super(ItemHistoryExportSerializer, self).to_representation(data)
        if data["type"] == FOLDER:
            data["size"] = count_size_of_folder(data["children"])
        data.pop("children")
        data["date"] = cut_date_to_format(data["date"])
        return data

    def get_fields(self):
        fields = super(ItemHistoryExportSerializer, self).get_fields()
        fields["children"] = ItemStructureExportSerializer(many=True)
        return fields

    class Meta:
        model = Item
        fields = ("id", "date", "url", "parentId", "type", "size")
