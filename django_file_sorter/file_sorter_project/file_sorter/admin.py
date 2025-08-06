from django.contrib import admin
from .models import SortingSession, SortedFile

@admin.register(SortingSession)
class SortingSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'folder_path', 'status', 'files_processed', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['folder_path']

@admin.register(SortedFile)
class SortedFileAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'destination_folder', 'file_type', 'sorted_at']
    list_filter = ['destination_folder', 'file_type']
    search_fields = ['original_name']