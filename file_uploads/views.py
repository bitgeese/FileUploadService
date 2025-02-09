from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.uploadedfile import UploadedFile
from typing import Any, Dict

from .models import FileUpload
from .serializers import FileUploadSerializer, FileListSerializer


class FileUploadView(generics.CreateAPIView):
    """Handle file uploads with metadata."""
    
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """Handle the file upload."""
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size (4GB-8GB)
        file_size = file_obj.size
        min_size = 4 * 1024 * 1024 * 1024  # 4GB
        max_size = 8 * 1024 * 1024 * 1024  # 8GB
        
        if not (min_size <= file_size <= max_size):
            return Response(
                {'error': 'File size must be between 4GB and 8GB'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create serializer with file and metadata
        serializer = self.get_serializer(data={
            'file': file_obj,
            'storage_path': request.data.get('storage_path', ''),
            'description': request.data.get('description', '')
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(generics.ListAPIView):
    """List all uploaded files."""
    
    queryset = FileUpload.objects.all()
    serializer_class = FileListSerializer 