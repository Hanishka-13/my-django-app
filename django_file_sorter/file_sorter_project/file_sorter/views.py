from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from pathlib import Path
from .services import FileSorterService
from .models import SortingSession, SortedFile
from .forms import FolderSelectForm

class HomeView(View):
    """Main view for file sorter"""
    
    def get(self, request):
        form = FolderSelectForm()
        recent_sessions = SortingSession.objects.order_by('-created_at')[:5]
        
        context = {
            'form': form,
            'recent_sessions': recent_sessions,
        }
        return render(request, 'file_sorter/home.html', context)

class SortFilesView(View):
    """Handle file sorting requests"""
    
    def post(self, request):
        form = FolderSelectForm(request.POST)
        
        if form.is_valid():
            folder_path = form.cleaned_data['folder_path']
            
            # Create file sorter service
            sorter = FileSorterService(folder_path=folder_path)
            
            # Perform sorting
            success, message = sorter.sort_files()
            
            if success:
                messages.success(request, message)
                return redirect('session_detail', session_id=sorter.session.id)
            else:
                messages.error(request, message)
        else:
            messages.error(request, "Please provide a valid folder path.")
        
        return redirect('home')

class SessionDetailView(View):
    """View sorting session details"""
    
    def get(self, request, session_id):
        session = get_object_or_404(SortingSession, id=session_id)
        sorted_files = session.sorted_files.all().order_by('destination_folder', 'original_name')
        
        # Group files by category
        files_by_category = {}
        for file in sorted_files:
            if file.destination_folder not in files_by_category:
                files_by_category[file.destination_folder] = []
            files_by_category[file.destination_folder].append(file)
        
        context = {
            'session': session,
            'files_by_category': files_by_category,
            'total_files': sorted_files.count()
        }
        return render(request, 'file_sorter/session_detail.html', context)