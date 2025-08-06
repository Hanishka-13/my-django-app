from django.db import models
from django.contrib.auth.models import User

class SortingSession(models.Model):
    """Track file sorting sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    folder_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    files_processed = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')

    def __str__(self):
        return f"Sorting session for {self.folder_path} - {self.status}"

class SortedFile(models.Model):
    """Track individual files that have been sorted"""
    session = models.ForeignKey(SortingSession, on_delete=models.CASCADE, related_name='sorted_files')
    original_name = models.CharField(max_length=255)
    original_path = models.CharField(max_length=500)
    destination_folder = models.CharField(max_length=100)
    destination_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=50)
    sorted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_name} -> {self.destination_folder}"