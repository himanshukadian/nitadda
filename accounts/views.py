from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from .admin import UserCreationForm
from django.contrib import messages
from content.models import *

def index(request):
    response = {}
    print(request.user," logged in : RENDER HOME ")
    note = Note.objects.all()[:5]
    lstatus = []
    providers = []
    for n in note:
        prv = CustomUser.objects.get(id=n.user_id)
        providers.append(prv.username)
        if n.upvotes.filter(id=request.user.id).exists():
            lstatus.append(True)
        else:
            lstatus.append(False)
    response['data'] = zip(note, lstatus, providers)
    # messages.add_message(request, 20, 'Login Successful!')
    # info = messages.get_messages(request)
    # response = {'message': info}
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
