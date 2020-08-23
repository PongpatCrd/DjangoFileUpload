from django.db import models
from django.utils.timezone import now

from .helper_functions import *

# Create your models here.
class Upload(models.Model):
    id               = models.AutoField(primary_key=True)
    password         = models.CharField(max_length=128, blank=True, null=True)
    max_downloads    = models.IntegerField()
    expire_date      = models.DateTimeField()
    is_active        = models.BooleanField(default=True)
    file             = models.FileField(upload_to=modify_name)
    ref_key_download = models.CharField(max_length=32, null=False, blank=False)
    ref_key_delete   = models.CharField(max_length=32, null=False, blank=False)
    created_at       = models.DateTimeField(default=now, editable=False)
    updated_at       = models.DateTimeField(auto_now=True)
    created_by       = models.CharField(max_length=25, null=False, blank=False)

    class Meta:
      db_table = 'upload'
      indexes = [
        models.Index(fields=['ref_key_download',]),
        models.Index(fields=['ref_key_delete',]),
        models.Index(fields=['expire_date', 'is_active']),
      ]

class DownloadLog(models.Model):
    id            = models.AutoField(primary_key=True)
    upload        = models.ForeignKey(Upload, on_delete=models.CASCADE)
    downloaded_by = models.CharField(max_length=25, null=False, blank=False)
    created_at    = models.DateTimeField(default=now, editable=False)

    class Meta:
      db_table = 'download_log'