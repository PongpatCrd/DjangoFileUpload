import os
import time

import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'send.settings'
django.setup()

from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from upload.models import *
from upload.helper_functions import *

while True:
  objects = Upload.objects.filter(
    Q(expire_date__lte=timezone.now(), is_active=True) |
    Q(max_downloads__lte=0, is_active=True)
  )
  list_file_name = list(objects.values_list('file', flat=True))
  
  objects.update(is_active=False)

  for file_name in list_file_name:
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    safe_delete_file(file_path)
  
  sleep_time_in_sec = 60
  time.sleep(sleep_time_in_sec)
