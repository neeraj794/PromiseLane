from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,update_session_auth_hash,get_user_model
from .models import ProImage
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db import transaction
from user_profile.models import MatrimonialProfile

User = get_user_model()

# Create your views here.
def fetch_pic(request):
    return get_object_or_404(ProImage,user=request.user)

def login_(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect(profile)
    else:
        form = AuthenticationForm()
    return render(request,'login.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                ProImage.objects.create(user=user)
            return redirect(login_)
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

@login_required
def logout_(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect(login_)

@login_required
def profile(request):
    pro_image = fetch_pic(request)
    matrimonial_profile = MatrimonialProfile.objects.filter(user=request.user).first()
    return render(request,'profile.html',{
        'pro_image':pro_image,
        'matrimonial_profile':matrimonial_profile,
    })

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect(login_)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,'update_password.html',{'form':form})

@login_required
def update_profile(request):
    userdata = request.user
    profiledata = get_object_or_404(ProImage,user=userdata)
    if request.method == 'POST':
        userform = UserUpdateForm(request.POST,instance=userdata)
        profileform = ProfileUpdateForm(request.POST,request.FILES,instance=profiledata)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect(profile)
    else:
        userform = UserUpdateForm(instance=userdata)
        profileform = ProfileUpdateForm(instance=profiledata)
    return render(request,'update_profile.html',{'user_form':userform,'profile_form':profileform})

def forgot_password(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            global username
            username = request.POST['username']
            try:
                user = User.objects.get(username=username)
                if User.objects.get(username=username):
                    messages.success(request,'Please Enter New Password')
                    return render(request,'forgot_password.html',{'new':True})
            except User.DoesNotExist:
                messages.error(request,'Invlid Username')
                return redirect('forgot_password')
        if 'newpasw' in request.POST:
            new_password = request.POST['newpasw']
            conf_password = request.POST['confpasw']
            if new_password != conf_password:
                messages.error(request,'new password must be equal to confirm password')
                return redirect('forgot_password')
            else:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password changed successfully')
                return redirect(login_)
    return render(request,'forgot_password.html')

@login_required
@require_POST
def toggle_profile_visibility(request):
    profile = get_object_or_404(MatrimonialProfile,user=request.user)
    profile.is_active = not profile.is_active
    profile.save()

    if profile.is_active:
        messages.success(request,"Your profile is now visible")
    else:
        messages.success(request,"Your profile is now hidden")

    return redirect('profile')