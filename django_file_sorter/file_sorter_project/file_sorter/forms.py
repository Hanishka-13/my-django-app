from django import forms
from pathlib import Path

class FolderSelectForm(forms.Form):
    folder_path = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter folder path (e.g., C:\\Users\\YourName\\Downloads)',
            'required': True
        }),
        help_text='Enter the full path to the folder containing files you want to sort.'
    )
    
    def clean_folder_path(self):
        folder_path = self.cleaned_data['folder_path']
        path = Path(folder_path)
        
        if not path.exists():
            raise forms.ValidationError("The specified folder does not exist.")
        
        if not path.is_dir():
            raise forms.ValidationError("The specified path is not a directory.")
        
        return folder_path