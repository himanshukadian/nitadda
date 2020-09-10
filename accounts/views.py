from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.shortcuts import resolve_url
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView
from django.utils.http import is_safe_url
from content.views import logout, checkuserifscrutinyuser
from django.template.loader import render_to_string
from base64 import urlsafe_b64encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import FormView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

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
    blogs = Blog.objects.all()
    for b in blogs:
        if len(b.description) > 300:
            b.description = b.description[:300]
    response['blogs'] = blogs
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
            mail_subject = 'Activate your NITADDA account.'
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
            email.content_subtype = 'html'
            try:
                email.send()
                messages.success(request,
                                 f'Your account has been created and you are logged in.Please confirm your email address to complete the registration')
            except:
                messages.success(request, f'Please enter valid email for registration')
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class UserUpdateFormView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'first_name', 'last_name', 'mobile', 'gender', 'image']
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
        response['user_has_liked_notes'] = True;
    else:
        response['user_has_liked_notes'] = False;
    response['liked_notes'] = liked_notes

    uploaded_notes = Note.objects.filter(user_id=request.user.id)
    uploaded_papers = Exam_Paper.objects.filter(user_id=request.user.id)
    uploaded_books = Book.objects.filter(user_id=request.user.id)


    response['uploaded_notes'] = uploaded_notes
    response['uploaded_papers'] = uploaded_papers
    response['uploaded_books'] = uploaded_books

    if len(uploaded_notes) > 0:
        response['user_has_uploaded_notes'] = True;
    else:
        response['user_has_uploaded_notes'] = False;
    if len(uploaded_papers) > 0:
        response['user_has_uploaded_papers'] = True;
    else:
        response['user_has_uploaded_papers'] = False;
    if len(uploaded_books) > 0:
        response['user_has_uploaded_books'] = True;
    else:
        response['user_has_uploaded_books'] = False;
    response['user'] = request.user
    return render(request, 'account/profile.html', response)


@csrf_exempt
def Contact_Us(request):
    if request.method == 'POST':
        print('Contact us message recieved.')
        newMessage = ContactUsMessage()
        newMessage.sender_name = request.POST['fullName']
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
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'account/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
