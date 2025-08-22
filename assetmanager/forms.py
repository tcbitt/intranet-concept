from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'asset_type',
            'model_type',
            'status_type',
            'checked_out_to_user',
            'checked_out_to_branch',
        ]
        labels = {
            'checked_out_to_user': 'User',
            'checked_out_to_branch': 'Branch',
            'status_type': 'Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Asset Name'}),
            'status_type': forms.Select(attrs={'class': 'form-select'}),
            'checked_out_to_user': forms.Select(attrs={'class': 'form-select'}),
            'checked_out_to_branch': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'checked_out_to_user': 'Select a user if this asset is assigned to someone.',
            'checked_out_to_branch': 'Or select a branch if it’s assigned to a location.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model_type'].queryset = self.fields['model_type'].queryset.order_by('name')
        if not self.instance.pk:
            from .models import Status
            self.fields['status_type'].initial = Status.objects.get(code='stock')

