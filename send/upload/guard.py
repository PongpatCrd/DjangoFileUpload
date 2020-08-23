from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone

def default_guard(obj_upload):
  print(obj_upload)
  if not obj_upload:
    return HttpResponseNotFound('This link not associated to any file.')
  
  if not obj_upload.is_active:
    return HttpResponseNotFound('File not exist anymore.')

  if obj_upload.expire_date < timezone.now() or obj_upload.max_downloads == 0:
    return HttpResponse('File already expired.')
  return None