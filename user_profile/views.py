from django.shortcuts import render,redirect,get_object_or_404
from .forms import MatrimonialProfileForm
from .models import MatrimonialProfile
from django.contrib import messages

# Create your views here.
def create_profile(request):
    profile = MatrimonialProfile.objects.filter(user=request.user).first()
    if profile:
        return redirect('update_user_profile')
    if request.method == 'POST':
        form = MatrimonialProfileForm(request.POST)
        if form.is_valid():
            matrimonial_profile = form.save(commit=False)
            matrimonial_profile.user = request.user
            matrimonial_profile.save()
            return redirect('profile')
    else:
        form = MatrimonialProfileForm()
    return render(request,'create_profile.html',{'form':form})

def update_user_profile(request):
    profile = MatrimonialProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = MatrimonialProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MatrimonialProfileForm(instance=profile)
    return render(request,'update_user_profile.html',{'form':form})