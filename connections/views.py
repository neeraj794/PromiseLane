from django.shortcuts import render,get_object_or_404,redirect
from user_profile.models import MatrimonialProfile
from django.contrib import messages
from .models import Interest,BlockedUser,Report
from django.contrib.auth.decorators import login_required
from authen.models import CustomUser
from django.db.models import Q
from .forms import ReportForm

# Create your views here.
@login_required
def send_interest(request,pk):
    if request.method == 'POST':
        profile = get_object_or_404(MatrimonialProfile,id=pk)
        receiver = profile.user
        if receiver == request.user:
            messages.error(request,"you cannot send interest to yourself.")

        elif BlockedUser.objects.filter(
            Q(blocker=request.user,blocked=receiver) |
            Q(blocker=receiver,blocked=request.user)
        ).exists():
            messages.error(request,'You cannot send interest to this user')

        elif Interest.objects.filter(sender=request.user,receiver=receiver).exists():
            messages.warning(request,"You have already sent request.")

        else:
            Interest.objects.create(sender=request.user,receiver=receiver)
            messages.success(request,"Interest sent successfully!")
        return redirect('profile_detail',pk=pk)
    return redirect('browse_profiles')

@login_required
def recieved_interests(request):
    interests = Interest.objects.filter(receiver=request.user).select_related('sender')
    return render(request,'received_interests.html',{'interests':interests})

@login_required
def respond_interests(request,pk):
    if request.method == 'POST':
        interest = get_object_or_404(Interest,id=pk,receiver=request.user)
        action = request.POST.get('action')
        if interest.status != 'Pending':
            messages.warning(request,"This interest has already been processed.")
        elif action == 'accept':
            interest.status = 'Accepted'
            interest.save()
            messages.success(request,"Interest accepted succesfully")
        elif action == 'reject':
            interest.status = 'Rejected'
            interest.save()
            messages.success(request,"Interest Rejected.")
    return redirect('received_interests')

@login_required
def sent_interests(request):
    interests = Interest.objects.filter(sender = request.user).select_related('receiver')
    return render(request,'sent_interests.html',{'interests':interests})

@login_required
def block_user(request,pk):
    if request.method == 'POST':
        user_to_block = get_object_or_404(CustomUser,id=pk)
        if user_to_block == request.user:
            messages.error(request,"You Cannot Block Yourself")
        else:
            BlockedUser.objects.get_or_create(blocker=request.user,blocked=user_to_block)
            messages.success(request,"User blocked Succesfully")
    return redirect('browse_profiles')

@login_required
def unblock_user(request,pk):
    if request.method == 'POST':
        blocked_user = get_object_or_404(BlockedUser,id=pk,blocker=request.user)
        blocked_user.delete()
        messages.success(request,"User unblocked successfully")
    return redirect('blocked_users')

@login_required
def blocked_users(request):
    blocked_list = BlockedUser.objects.filter(blocker=request.user).select_related('blocked')
    return render(request,'blocked_users.html',{'blocked_list':blocked_list})

@login_required
def report_profile(request,pk):
    profile = get_object_or_404(MatrimonialProfile,id=pk,is_active=True)
    reported_user = profile.user
    if reported_user == request.user:
        messages.error(request,'You cannot report your own profile')
        return redirect('browse_profiles')
    is_blocked = BlockedUser.objects.filter(
        Q(blocker=request.user,blocked=reported_user) |
        Q(blocker=reported_user,blocked=request.user)
    ).exists()

    if is_blocked:
        messages.error(request,"You cannot report this profile")
        return redirect('browse_profiles')

    if request.method == 'POST':
        already_reported = Report.objects.filter(
            reporter=request.user,
            reported_user=reported_user,
            status='Pending'
        ).exists()

        if already_reported:
            messages.warning(request,"You have already reported this profile.")
            return redirect('profile_detail',pk=pk)
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.save()
            messages.success(request,"Profile reported successfully.")
            return redirect('profile_detail',pk=pk)
    else:
        form = ReportForm()
    return render(request,'report_profile.html',{'form':form,'profile':profile})