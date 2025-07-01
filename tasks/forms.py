from django import forms
from .models import Task, TaskList

class TaskForm(forms.ModelForm):
    """For creating and editing tasks"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'task_list']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter task description (optional)'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'task_list': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter task lists to show only user's lists
        if user:
            self.fields['task_list'].queryset = TaskList.objects.filter(user=user)
            self.fields['task_list'].required = False
            self.fields['task_list'].empty_label = "My Tasks"
            