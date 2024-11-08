from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms.widgets import DateInput, Select

from .models import CustomUser, UserProfile


class SignUpMainForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'site_url')

    def clean_site_url(self):
        """Reject usernames that differ only in case."""
        site_url = self.cleaned_data.get("site_url")
        if site_url and self._meta.model.objects.filter(site_url__iexact=site_url).exists():
            last_url = self._meta.model.objects.filter(site_url__startswith=site_url).order_by('-date_joined')[0]
            try:
                num = int(last_url.site_url[len(site_url):])
            except ValueError:
                num = 1
            site_url = f'{site_url}{num + 1}'
        return site_url


class SignUpSecondaryDataForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'gender')

    widgets = {
        'date_of_birth': DateInput(attrs={'type': 'date'}),
        'gender': Select(),
    }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')


class UserProfileChangeForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'gender', 'bio', 'place_of_live', 'occupation')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'gender': Select(),
        }
