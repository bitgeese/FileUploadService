from django.urls import path
from .views import FileUploadView, FileListView

app_name = 'file_uploads'

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('', FileListView.as_view(), name='file-list'),
] 