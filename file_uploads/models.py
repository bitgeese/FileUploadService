from django.db import models
from django.core.validators import FileExtensionValidator
from typing import Any


class FileUpload(models.Model):
    """Model for storing uploaded file metadata."""
    
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'tar', 'gz'])]
    )
    original_filename = models.CharField(max_length=255)
    storage_path = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField()
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['-uploaded_at']),
            models.Index(fields=['storage_path']),
        ]
    
    def __str__(self) -> str:
        return f"{self.original_filename} ({self.size_bytes} bytes)"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to ensure storage path is set."""
        if not self.storage_path:
            self.storage_path = f"uploads/{self.file.name}"
        super().save(*args, **kwargs) 