from django.urls import path
from . import views

urlpatterns = [
  path('', views.UploadView.as_view(), name="upload"),
  path("<slug:ref_key_download>", views.DownloadView.as_view(), name="download"),
  path("delete/<slug:ref_key_delete>", views.DeleteView.as_view(), name="delete"),
]
