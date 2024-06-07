from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from users.forms import ProfileForm, EmailForm

User = get_user_model()


def profile(request, username=None):
    if username:
        user_profile = get_object_or_404(User, username=username).profile
    else:
        try:
            user_profile = request.user.profile
        except AttributeError:
            # If the user does not have a profile, redirect to login
            return redirect('account_login')
    return render(request, 'users/profile.html', {'profile': user_profile})


@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')

    # Default value for onboarding if not in 'POST' request
    onboarding = request.path == reverse('users:profile_onboarding')
    return render(request, 'users/profile_edit.html', {'form': form, 'onboarding': onboarding})


@login_required
def profile_settings(request):
    return render(request, 'users/profile_settings.html')


@login_required
def profile_email_change(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Send email confirmation
            send_email_confirmation(request, request.user)
        else:
            email = request.user.email
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('users:profile_settings')

    # Redirect to profile settings page after form submission
    return redirect('users:profile_settings')


@login_required
def profile_email_verify(request):
    send_email_confirmation(request, request.user)
    return redirect('users:profile_settings')


@login_required
def profile_delete(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('chats:home')

    return render(request, 'users/profile_delete.html')
