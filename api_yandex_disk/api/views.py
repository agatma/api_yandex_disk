from datetime import datetime, timedelta
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.models import Item, FILE
from api.serializers import (
    ItemImportSerializer,
    ItemStructureExportSerializer,
    ItemExportSerializer,
    ItemHistoryExportSerializer,
)
from api.validation import items_validation
from api.utils import update_parent_date

OpenAPI_datetime_pattern = "%Y-%m-%dT%H:%M:%S.%fZ"


class ItemImportView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemImportSerializer

    def create(self, request, *args, **kwargs):
        try:
            items = request.data["items"]
            update_date = request.data["updateDate"]
        except KeyError as e:
            raise ValidationError() from e
        try:
            update_date = datetime.strptime(update_date, OpenAPI_datetime_pattern)
        except ValueError as e:
            raise ValidationError() from e
        if not items_validation(items):
            raise ValidationError()
        serializer = self.get_serializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(date=update_date)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ItemExportView(generics.RetrieveAPIView):
    serializer_class = ItemStructureExportSerializer

    def get_object(self):
        return get_object_or_404(Item, pk=self.kwargs["item_uuid"])


class ItemHistoryExportView(generics.RetrieveAPIView):
    serializer_class = ItemHistoryExportSerializer

    def get_object(self):
        start_dt = self.request.query_params.get("dateStart")
        end_dt = self.request.query_params.get("dateEnd")
        if not start_dt and not end_dt:
            return get_object_or_404(Item, pk=self.kwargs["item_uuid"])
        if start_dt and not end_dt:
            try:
                start_dt = datetime.strptime(start_dt, OpenAPI_datetime_pattern)
            except (ValueError, TypeError) as e:
                print("Произошла ошибка")
                raise ValidationError() from e
            try:
                return Item.objects.get(pk=self.kwargs["item_uuid"], date__gte=start_dt)
            except Item.DoesNotExist as e:
                raise ValidationError() from e
        if end_dt:
            try:
                end_dt = datetime.strptime(end_dt, OpenAPI_datetime_pattern)
            except (ValueError, TypeError) as e:
                raise ValidationError() from e
            try:
                return Item.objects.get(
                    pk=self.kwargs["item_uuid"], date__gte=start_dt, date__lte=end_dt
                )
            except Item.DoesNotExist as e:
                raise ValidationError() from e

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"items": [serializer.data]})


class ItemDeleteView(generics.DestroyAPIView):
    def get_object(self):
        return get_object_or_404(Item, pk=self.kwargs["item_uuid"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        dt = self.request.query_params.get("date")
        try:
            dt = datetime.strptime(dt, OpenAPI_datetime_pattern)
        except (ValueError, TypeError) as e:
            raise ValidationError() from e
        update_parent_date(instance, dt)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class Item24HourUpdateView(generics.ListAPIView):
    serializer_class = ItemExportSerializer

    def get_queryset(self):
        end_dt = self.request.query_params.get("date")
        try:
            start_dt = datetime.strptime(end_dt, OpenAPI_datetime_pattern) - timedelta(
                days=1
            )
        except (ValueError, TypeError) as e:
            raise ValidationError() from e
        return Item.objects.filter(type=FILE, date__gte=start_dt, date__lte=end_dt)
