import os
import shutil
from pathlib import Path
from django.utils import timezone
from .models import SortingSession, SortedFile

class FileSorterService:
    """File sorting service with Django integration"""
    
    FILE_TYPES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
        'Documents': ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt'],
        'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
        'Videos': ['.mp4', '.mkv', '.mov', '.avi', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.php', '.java', '.cpp'],
        'Others': []
    }
    
    def __init__(self, folder_path, user=None):
        self.folder_path = Path(folder_path)
        self.user = user
        self.session = None
    
    def create_session(self):
        """Create a new sorting session"""
        self.session = SortingSession.objects.create(
            user=self.user,
            folder_path=str(self.folder_path),
            status='pending'
        )
        return self.session
    
    def create_folder(self, folder_name):
        """Create folder if it doesn't exist"""
        folder_path = self.folder_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path
    
    def get_file_category(self, file_extension):
        """Determine file category based on extension"""
        file_ext = file_extension.lower()
        for category, extensions in self.FILE_TYPES.items():
            if file_ext in extensions:
                return category
        return 'Others'
    
    def sort_files(self):
        """Main file sorting function"""
        if not self.session:
            self.create_session()
        
        self.session.status = 'processing'
        self.session.save()
        
        try:
            files_processed = 0
            
            for file_path in self.folder_path.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    file_category = self.get_file_category(file_ext)
                    
                    # Create destination folder
                    dest_folder = self.create_folder(file_category)
                    dest_path = dest_folder / file_path.name
                    
                    # Handle filename conflicts
                    counter = 1
                    original_dest_path = dest_path
                    while dest_path.exists():
                        stem = original_dest_path.stem
                        suffix = original_dest_path.suffix
                        dest_path = dest_folder / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    # Move the file
                    shutil.move(str(file_path), str(dest_path))
                    
                    # Record in database
                    SortedFile.objects.create(
                        session=self.session,
                        original_name=file_path.name,
                        original_path=str(file_path),
                        destination_folder=file_category,
                        destination_path=str(dest_path),
                        file_size=dest_path.stat().st_size,
                        file_type=file_ext
                    )
                    
                    files_processed += 1
            
            # Update session
            self.session.files_processed = files_processed
            self.session.status = 'completed'
            self.session.completed_at = timezone.now()
            self.session.save()
            
            return True, f"Successfully sorted {files_processed} files"
            
        except Exception as e:
            self.session.status = 'failed'
            self.session.save()
            return False, f"Error sorting files: {str(e)}"