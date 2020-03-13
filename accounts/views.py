from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from .admin import UserCreationForm
from django.contrib import messages


def index(request):
    response = {}
    return render(request, 'home.html', response)


class UserFormView(generic.View):
    form_class = UserCreationForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            messages.success(request, f'Your account has been created')
            return redirect('accounts:index')

        return render(request, self.template_name, {'form': form})


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.success(request, f'You are loged in')
            return redirect('accounts:index')
