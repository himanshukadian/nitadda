from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.http import HttpResponse

from django.views.generic import UpdateView
from django.utils.http import is_safe_url
from content.views import logout, checkuserifscrutinyuser
from django.template.loader import render_to_string
from venv.Lib.base64 import urlsafe_b64encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



from nitadda.tokens import account_activation_token
from .admin import UserCreationForm
from django.contrib import messages
from content.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage



def index(request):
    response = {}
    print(request.user, " logged in : RENDER HOME ")
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
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

        return render(request, self.template_name, {'form': form})


class UserUpdateFormView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'first_name','last_name', 'mobile', 'gender', 'image']
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
        next_post = request.POST.get('next')
        redirect_path = next_post
        username = request.POST['username']
        try:
            username = CustomUser.objects.get(email=username).username
        except CustomUser.DoesNotExist:
                username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You are successfully logged in.')
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
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


@csrf_exempt
def Contact_Us(request):
    if request.method == 'POST':
        print('Contact us message recieved.')
        newMessage = ContactUsMessage()
        newMessage.sender_name = request.POST['fullast_name']
        newMessage.email = request.POST['email']
        newMessage.phone = request.POST['phone']
        newMessage.subject = request.POST['subject']
        newMessage.message = request.POST['message']
        superuser = CustomUser.objects.filter(is_superuser=True).first()
        superuser.notifications = superuser.notifications + 1
        superuser.noti_messages = superuser.noti_messages + '<li> New message has arrived in inbox </li>'
        superuser.save()
        newMessage.save()
        messages.add_message(request, messages.INFO, 'Your Message has been sent. We will email you back soon.')
        return redirect('accounts:index')
    else:
        print('Contact us message ERROR.')
        return render(request, 'home.html')


@csrf_exempt
@login_required(login_url="accounts:login")
@user_passes_test(checkuserifscrutinyuser, login_url="accounts:login")
def Inbox(request):
    print('Inbox tab has opened.')
    all_messages = ContactUsMessage.objects.all()
    response = {}
    if (len(all_messages) > 0):
        response['admin_has_messages'] = True
    else:
        response['admin_has_messages'] = False
    response['all_messages'] = all_messages;

    return render(request, 'account/inbox.html', response)


@csrf_exempt
@login_required(login_url="accounts:login")
@user_passes_test(checkuserifscrutinyuser, login_url="accounts:login")
def Show_Message(request):
    response = {}
    mid = request.GET['message_id']
    print('Message having ID ', mid, ' has been opened.')
    mes = get_object_or_404(ContactUsMessage, pk=mid)
    if mes:
        mes.has_been_read = True
        mes.save()
        response['message'] = mes
        return render(request, 'account/show_inbox_message.html', response)
    else:
        return render(request, 'account/inbox.html', response)


@csrf_exempt
@login_required(login_url="accounts:login")
@user_passes_test(checkuserifscrutinyuser, login_url="accounts:login")
def Mark_As_Read(request):
    mid = request.GET['message_id']
    print('Message having ID ', mid, ' has been marked as read.')
    mes = get_object_or_404(ContactUsMessage, pk=mid)
    mes.has_been_read = True
    mes.save()
    return redirect('accounts:inbox')


@csrf_exempt
@login_required(login_url="accounts:login")
@user_passes_test(checkuserifscrutinyuser, login_url="accounts:login")
def Delete_Message(request):
    mid = request.GET['message_id']
    print('Message having ID ', mid, ' has been deleted.')
    mes = get_object_or_404(ContactUsMessage, pk=mid)
    mes.delete()
    messages.success(request, 'Message has been successfully deleted.')
    return redirect('accounts:inbox')


@login_required
def clear(request, pk):
    user = request.user
    user.noti_messages = ''
    user.notifications = 0
    user.save()
    messages.success(request, f'All notifications cleared')
    return redirect('/')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
