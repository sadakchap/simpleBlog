from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash

from social_django.models import UserSocialAuth

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm

from django.contrib import messages
from django.contrib.auth.models import User

from accounts.tokens import account_activation_token

# Create your views here.

def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        subject = "Activate Your 'Django Blog' Account" 
        msg = render_to_string('account_activation_email.html',{
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, msg)
        messages.success(request,f'Your account has been Created.Please Confirm your Email!')
        return redirect('account_activation_sent')

    return render(request,'accounts/register.html',{'form':form})

@login_required
def profile(req):
    u_form = UserUpdateForm(req.POST or None,instance=req.user)
    p_form = ProfileUpdateForm(req.POST or None,req.FILES or None,instance=req.user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(req,'Profile Updated!')
        return redirect('profile')
    context = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(req,'accounts/profile.html',context)


def account_activation_sent(request):
    return render(request,'accounts/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    print(user)
    print(account_activation_token.check_token(user, token))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        print('active')
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request,f'{user.username.capitalize()}, your email is confirmed')
        return redirect('blog-home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


@login_required
def settings(request):
    user = request.user
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None
    print(google_login, google_login.extra_data, sep='\n')
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'accounts/settings.html', {
        'google_login': google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please enter the correct below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.html', {'form':form})