from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from .admin import UserCreationForm
from django.contrib import messages


def index(request):
    info = messages.get_messages(request)
    response = {'message': info}
    print("msg :", info)
    return render(request, 'home.html', response)


class UserFormView(generic.View):
    form_class = UserCreationForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been successfully created.')
            return redirect('accounts:index')

        return render(request, self.template_name, {'form': form})


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    print("no. 1")
    if user is not None:
        print("no. 2")
        if user.is_active:
            print("no. 3")
            login(request, user)
            messages.success(request, 'You are successfully logged in.')
            return redirect('accounts:index')
        return render(request, "signin.html")
    return render(request, "signin.html")
