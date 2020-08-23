import uuid
import os

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

def create_hex_key():
  return uuid.uuid4().hex

def modify_name(instance, name):
  return f'{create_hex_key()}_{name}'

def de_modify_name(name):
  base_name = os.path.basename(name)
  return base_name[base_name.find('_')+1:]

def safe_delete_file(file_path):
  try:
    os.remove(file_path)
  except:
    pass
  return
