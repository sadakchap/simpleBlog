from django.shortcuts import render,redirect
from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def register(req):
    form = UserRegisterForm(req.POST or None)
    if form.is_valid():
        form.save()
        unm = form.cleaned_data.get('username')
        messages.success(req,f'Your account has been Created . You can Login!')
        return redirect('login')

    return render(req,'accounts/register.html',{'form':form})

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
