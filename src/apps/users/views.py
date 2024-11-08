from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import SignUpMainForm, SignUpSecondaryDataForm
from apps.chat.models import LastVisitedRoom
from apps.common import utils as cleanups


# Class based views


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        cleanups.temporary_data_cleanup(request.user)

        return super().dispatch(request, *args, **kwargs)


# Function based views

def signup(request):
    if request.method == 'POST':
        site_url = f"{request.POST['first_name']}.{request.POST['last_name']}".lower()
        main_form_extended_data = request.POST.copy()
        main_form_extended_data['site_url'] = site_url

        form_main = SignUpMainForm(main_form_extended_data)
        form_secondary = SignUpSecondaryDataForm(request.POST)
        if form_main.is_valid() and form_secondary.is_valid():
            user = form_main.save()
            form_secondary = form_secondary.save(commit=False)
            form_secondary.user = user
            form_secondary.save()
            LastVisitedRoom.objects.create(user=user)
            login(request, user)
            return redirect('core:main')
    else:
        form_main = SignUpMainForm()
        form_secondary = SignUpSecondaryDataForm()

    context = {
        'form_main': form_main,
        'form_secondary': form_secondary,
    }
    return render(request, 'users/signup.html', context)
