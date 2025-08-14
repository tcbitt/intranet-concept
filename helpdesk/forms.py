from django import forms
from .models import Ticket, TicketComment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Brief summary of the issue',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the problem in detail...',
                'class': 'form-control',
                'rows': 5
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Add a comment...',
                'class': 'form-control',
                'rows': 3
            }),
        }
