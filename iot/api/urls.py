from django.urls import path

from .views import SensorReadingListView, SensorReadingUploadView

urlpatterns = [
    path(
        "readings/upload/",
        SensorReadingUploadView.as_view(),
        name="sensor-reading-upload",
    ),
    path("readings/", SensorReadingListView.as_view(), name="sensor-reading-list"),
]
