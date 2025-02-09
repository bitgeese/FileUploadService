from rest_framework import serializers
from .models import FileUpload
from typing import Dict, Any


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for file uploads."""
    
    class Meta:
        model = FileUpload
        fields = [
            'id',
            'file',
            'original_filename',
            'storage_path',
            'size_bytes',
            'content_type',
            'uploaded_at',
            'description'
        ]
        read_only_fields = ['id', 'uploaded_at', 'size_bytes', 'content_type']
    
    def create(self, validated_data: Dict[str, Any]) -> FileUpload:
        """Handle file upload and metadata."""
        file_obj = validated_data['file']
        
        # Set additional metadata
        validated_data['original_filename'] = file_obj.name
        validated_data['size_bytes'] = file_obj.size
        validated_data['content_type'] = file_obj.content_type
        
        return super().create(validated_data)


class FileListSerializer(serializers.ModelSerializer):
    """Serializer for listing uploaded files."""
    
    class Meta:
        model = FileUpload
        fields = [
            'id',
            'original_filename',
            'storage_path',
            'size_bytes',
            'content_type',
            'uploaded_at',
            'description'
        ] 