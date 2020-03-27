from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import UpdateView

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
    template_name = 'account/registration_form.html'

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


class UserUpdateFormView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'name', 'mobile', 'gender', 'registration_number', 'image']
    template_name = 'account/registration_form.html'

    def form_valid(self, form):
        form.instance.by = str(self.request.user)
        messages.success(self.request, f'Your account has been updated!')
        return super().form_valid(form)

    def test_func(self):
        customUser = str(self.get_object())
        user = str(self.request.user)
        if user == customUser:
            return True
        return False


def user_login(request):
    response = {}
    if request.user.is_authenticated:
        logout(request)
    else:
        response = {}
        if request.method == 'POST':
            username = request.POST['username']
            try:
                username = CustomUser.objects.get(email=username).username
            except CustomUser.DoesNotExist:
                try:
                    username = CustomUser.objects.get(registration_number=username).username
                except CustomUser.DoesNotExist:
                    username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You are successfully logged in.')
                    return redirect('accounts:index')
                else:
                    messages.warning(request, 'User is not active yet')
                    response['message'] = 'User is not active yet'
            else:
                messages.warning(request, 'User is invalid')
                response['message'] = 'User is invalid'

        return render(request, 'account/signin.html', response)


@login_required(login_url='/content/login')
def profile(request):
    all_notes = Note.objects.all()
    liked_notes = []
    lstatus = []
    providers = []
    response = {}
    for note in all_notes:
        if note.upvotes.filter(id=request.user.id).exists():
            liked_notes.append(note)
            prv = CustomUser.objects.get(id=note.user_id)
            providers.append(prv.username)
            lstatus.append(True)

    response['data1'] = zip(liked_notes, lstatus, providers)
    if len(liked_notes) > 0:
        response['user_has_liked'] = True;
    else:
        response['user_has_liked'] = False;
    uploaded_notes = Note.objects.filter(user_id=request.user.id)
    response['data'] = uploaded_notes
    if len(uploaded_notes) > 0:
        response['user_has_uploaded'] = True;
    else:
        response['user_has_uploaded'] = False;
    response['user'] = request.user
    return render(request, 'account/profile.html', response)
