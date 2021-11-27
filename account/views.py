from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.storage import FileSystemStorage
import datetime
from django.core import mail
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .tokens import account_activation_token


# Create your views here.

def test(request):

    return render(request, 'account/base.html')


def user_login(request):

    # we request the user
    a_user = request.user

    if a_user.is_authenticated:
        message = "Login"

        return render(request, 'account/login_already.html', {'user': a_user, 'message': message})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request,
                                    username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('index')
                    else:
                        messages.warning(request, "Account not active !!")

                        return redirect('login')
                else:
                    messages.warning(request, "Please enter a correct username and password. Note that both fields may be case-sensitive.")
                    return redirect('login')
                    # return HttpResponse('Invalid login')
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'form': form})


def register(request):
    try:
        allow = AllowRegistration.objects.all()

        if allow.count() > 0:

            allow_register = AllowRegistration.objects.get(id=1).status

            # we request the user
            a_user = request.user

            if a_user.is_authenticated:
                message = "Register"

                return render(request, 'account/login_already.html', {'user': a_user, 'message': message})

            else:
                if allow_register:

                    if request.method == 'POST':
                        user_form = UserRegistrationForm(request.POST)

                        if user_form.is_valid():
                            # Create a new user object but avoid saving it yet
                            new_user = user_form.save(commit=False)

                            cd = user_form.cleaned_data

                            if cd['password'] != cd['password2']:
                                # raise forms.ValidationError('Passwords don\'t match.')
                                # return cd['password2']

                                messages.warning(request, "Unsuccessful registration. Please make sure your passwords match.")

                                return redirect('register')
                            else:
                                # Set the chosen password
                                new_user.set_password(
                                    user_form.cleaned_data['password'])

                                # we deactivate the account until email confirmation
                                new_user.is_active = False

                                # Save the User object
                                new_user.save()

                                current_site = get_current_site(request)

                                """ 
                                mail_subject = 'Activate Your Account.' 
                                message = render_to_string('account/acc_active_emailBad.html', {
                                    'user': new_user,
                                    'domain': current_site.domain,
                                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                                    # 'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                    'token':account_activation_token.make_token(new_user),
                                })
                                to_email = cd['email']
                                email = EmailMessage(mail_subject, message, to=[to_email])
                                email.send()
                                """

                                subject = 'Activate Your Account.'
                                html_message = render_to_string('account/acc_active_emailBad.html',
                                {
                                    'user': new_user,
                                    'domain': current_site.domain,
                                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                                    # 'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                    'token': account_activation_token.make_token(new_user),
                                })
                                plain_message = strip_tags(html_message)
                                from_email = settings.EMAIL_HOST_USER
                                to = cd['email']

                                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

                                return render(request, 'account/register_done.html', {'new_user': new_user})
                        else:
                            user_form = request.POST

                            if user_form.get('password') != user_form.get('password2'):

                                messages.warning(request, "Unsuccessful registration. Please make sure your passwords match.")

                                return redirect('register')

                            messages.warning(request, "Ooops. Something went wrong ... Try again. ")
                            return redirect('register')
                    else:
                        user_form = UserRegistrationForm()
                        return render(request, 'account/register.html', {'user_form': user_form})
                else:
                    return render(request, 'account/no_register.html')

    except AllowRegistration.DoesNotExist:
        pass


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        messages.success(request, "Your Account has been successfully activated ! ")
        return redirect('index')
    else:
        return HttpResponse('Activation link is invalid! Contact your Admin.')


@login_required(redirect_field_name='login')
@require_GET
def profile(request):
    template_name = 'account/profile.html'
    user_form = UserEditForm(instance=request.user)
    pform = PasswordChangeForm(request.user)
    context = {'user_form': user_form, 'pform': pform}

    return render(request, template_name, context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        
        if user_form.is_valid():  
            # we request the user
            user = request.user

            profile_form = user_form.save(commit=False)

            user.username = profile_form.username
            user.first_name = profile_form.first_name
            user.last_name = profile_form.last_name
            user.email = profile_form.email

            if request.POST.get('date_of_birth'):
                user.date_of_birth = request.POST.get('date_of_birth')

            if request.FILES.get('photo'):
                user.photo = request.FILES.get('photo')

            profile_form.save()
            user.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.warning(request, 'Error updating your profile')
            
        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        
    return redirect('profile')


@login_required(redirect_field_name='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.warning(request, 'Please correct the error below.')

    # on change l'URL, de settings vers profile
    return redirect(reverse('profile') + '#navtabs-profile')


@login_required 
def change_status_registration(request):
    
    # we request the user
    user = request.user

    if user.is_staff:
        allow_register = AllowRegistration.objects.get(id=1)
        if allow_register.status:
            allow_register.status = False
        else:
            allow_register.status = True
        
        allow_register.save()

    return redirect('/')

