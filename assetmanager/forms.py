from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name',
            'asset_type',
            'model_type',
            'checked_out_to_user',
            'checked_out_to_branch',
        ]
        labels = {
            'checked_out_to_user': 'User',
            'checked_out_to_branch': 'Branch',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Asset Name'}),
        }

