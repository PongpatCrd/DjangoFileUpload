from django.http import HttpResponse, StreamingHttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils import timezone

import os
import mimetypes
from wsgiref.util import FileWrapper

from .forms import *
from .helper_functions import *
from .guard import *
from upload.models import *

class UploadView(CreateView):
  template_name = 'upload/upload_form.html'
  success_url   = reverse_lazy('upload')
  form_class    = UploadForm

  def form_valid(self, form):
    self.object                  = form.save(commit=False)
    self.object.password         = make_password(form.data.get('password', None))
    self.object.expire_date      = timezone.now() + timezone.timedelta(seconds=int(form.data.get('expire_duration')))
    self.object.ref_key_download = create_hex_key()
    self.object.ref_key_delete   = create_hex_key()
    self.object.created_by       = get_client_ip(self.request)
    self.object.save()
    try:
      self.object.save()
    except:
      return HttpResponse(status=500)

    download_url = self.request.build_absolute_uri(
      reverse('download', kwargs={'ref_key_download': self.object.ref_key_download})
    )

    delete_url = self.request.build_absolute_uri(
      reverse('delete', kwargs={'ref_key_delete': self.object.ref_key_delete})
    )
    context = {
      'form'        : form,
      'download_url': download_url,
      'delete_url'  : delete_url
    }
    return self.render_to_response(context)

class DownloadDetailView(DetailView):
  template_name       = 'upload/download_form.html'
  slug_field          = 'ref_key_download'
  slug_url_kwarg      = 'ref_key_download'
  model               = Upload

  def get(self, request, *args, **kwargs):
    try:
      self.object = self.get_object()
    except:
      self.object = None

    guard_response = default_guard(self.object)
    if guard_response:
      return guard_response

    context = self.get_context_data(object=self.object)
    return self.render_to_response(context)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    if check_password('', self.object.password):
      context['password'] = False
    else:
      context['password'] = True

    context['filename'] = de_modify_name(self.object.file.name)
    context['form']     = DownloadForm()
    return context

class DownloadInterest(SingleObjectMixin, FormView):
  template_name  = 'upload/download_form.html'
  slug_field     = 'ref_key_download'
  slug_url_kwarg = 'ref_key_download'
  form_class     = DownloadForm
  model          = Upload

  def form_valid(self, form):
    return self.post(self.request)

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()

    guard_response = default_guard(self.object)
    if guard_response:
      return guard_response
    
    if not check_password(request.POST.get('password', ''), self.object.password):
      return HttpResponse('Password not match')

    self.object.max_downloads -= 1
    self.object.save()
    
    DownloadLog.objects.create(
      upload        = self.object,
      downloaded_by = get_client_ip(request)
    )

    file_path = self.object.file.path
    filename = de_modify_name(os.path.basename(file_path))
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(file_path, 'rb'), chunk_size),
                            content_type=mimetypes.guess_type(file_path)[0])
    response['Content-Length'] = os.path.getsize(file_path)    
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

class DownloadView(View):
  def get(self, request, *args, **kwargs):
      view = DownloadDetailView.as_view()
      return view(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      view = DownloadInterest.as_view()
      return view(request, *args, **kwargs)

class DeleteView(DetailView):
  model = Upload
  template_name = 'upload/delete_form.html'
  slug_field     = 'ref_key_delete'
  slug_url_kwarg = 'ref_key_delete'
  
  def post(self, *args, **kwargs):
    self.object = self.get_object()
    if self.object:
      if self.object.is_active:
        self.object.is_active = False
        self.object.save()
        
        file_path = os.path.join(settings.MEDIA_ROOT, self.object.file.name)
        safe_delete_file(file_path)
    return HttpResponse('Deleted!')
  
  def get(self, request, *args, **kwargs):
    try:
      self.object = self.get_object()
    except:
      self.object = None

    guard_response = default_guard(self.object)
    if guard_response:
      return guard_response

    context = self.get_context_data(object=self.object)
    return self.render_to_response(context)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filename'] = de_modify_name(self.object.file.name)
    return context
