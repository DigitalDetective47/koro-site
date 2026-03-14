from django.urls import path

from .views import download, item

urlpatterns = [
    path("<int:pk>", item, name="item"),
    path("<int:pk>/download", download, name="download"),
]
