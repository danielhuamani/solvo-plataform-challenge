from django.urls import path

from apps.devices.views import DeviceListCreateView

urlpatterns = [
    path("", DeviceListCreateView.as_view(), name="devices-list-create"),
]
