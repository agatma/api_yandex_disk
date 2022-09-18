from django.urls import path

from api.views import (
    ItemImportView,
    ItemExportView,
    ItemDeleteView,
    Item24HourUpdateView,
    ItemHistoryExportView,
)


urlpatterns = [
    path(r"imports", ItemImportView.as_view()),
    path(r"node/<uuid:item_uuid>/history", ItemHistoryExportView.as_view()),
    path(r"nodes/<uuid:item_uuid>", ItemExportView.as_view()),
    path(r"delete/<uuid:item_uuid>", ItemDeleteView.as_view()),
    path(r"updates", Item24HourUpdateView.as_view()),
]
