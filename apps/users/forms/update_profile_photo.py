from django import forms

from apps.users.models import Profile


class UpdateProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={'id': 'formFile', 'accept': '.jpg,.jpeg,.png'})
        }
