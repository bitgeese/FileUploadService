import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from ..models import FileUpload


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_file():
    """Create a test file."""
    file_content = os.urandom(4 * 1024 * 1024 * 1024)  # 4GB file
    return SimpleUploadedFile(
        name='test_file.txt',
        content=file_content,
        content_type='text/plain'
    )


@pytest.mark.django_db
class TestFileUploadView:
    def test_upload_file_success(self, api_client, sample_file):
        """Test successful file upload."""
        url = reverse('file_uploads:file-upload')
        data = {
            'file': sample_file,
            'storage_path': '/storage/test',
            'description': 'Test file upload'
        }
        
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert FileUpload.objects.count() == 1
        assert FileUpload.objects.first().original_filename == 'test_file.txt'
    
    def test_upload_file_no_file(self, api_client):
        """Test file upload without file."""
        url = reverse('file_uploads:file-upload')
        data = {
            'storage_path': '/storage/test',
            'description': 'Test file upload'
        }
        
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert FileUpload.objects.count() == 0


@pytest.mark.django_db
class TestFileListView:
    def test_list_files_empty(self, api_client):
        """Test listing files when no files exist."""
        url = reverse('file_uploads:file-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
    
    def test_list_files_with_data(self, api_client, sample_file):
        """Test listing files with existing files."""
        # First upload a file
        upload_url = reverse('file_uploads:file-upload')
        data = {
            'file': sample_file,
            'storage_path': '/storage/test',
            'description': 'Test file upload'
        }
        api_client.post(upload_url, data, format='multipart')
        
        # Then list files
        list_url = reverse('file_uploads:file-list')
        response = api_client.get(list_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['original_filename'] == 'test_file.txt' 