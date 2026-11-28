from django.shortcuts import render,get_object_or_404,redirect
from user_profile.models import MatrimonialProfile
from django.contrib import messages
from .models import Interest,BlockedUser,Report,PartnerPreFerences
from django.contrib.auth.decorators import login_required
from authen.models import CustomUser
from django.db.models import Q
from .forms import ReportForm,PartnerPreFerenceForm

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

@login_required
def partner_preferences(request):
    preference, created = PartnerPreFerences.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PartnerPreFerenceForm(request.POST,instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request,"Partner preferences saved successfully.")
            return redirect('matches')
    else:
        form = PartnerPreFerenceForm(instance=preference)
    return render(request,'partner_preferences.html',{'form': form})


from datetime import date, timedelta
import calendar


def subtract_years(value, years):
    try:
        return value.replace(year=value.year - years)
    except ValueError:
        # Handles February 29 in leap years
        last_day = calendar.monthrange(
            value.year - years,
            value.month
        )[1]


        return value.replace(
            year=value.year - years,
            day=last_day
        )




@login_required
def matches(request):
    preference, created = PartnerPreFerences.objects.get_or_create(user=request.user)
    today = date.today()
    # Calculate DOB range from preferred age range
    latest_dob = subtract_years(today,preference.min_age)
    earliest_dob = subtract_years(
        today,
        preference.max_age + 1
    ) + timedelta(days=1)


    profiles = MatrimonialProfile.objects.filter(
        is_active=True,
        user__dob__range=(earliest_dob,latest_dob)
    ).exclude(
        user=request.user
    ).select_related(
        'user'
    )


    # Preferred gender
    if preference.preferred_gender != 'Any':
        profiles = profiles.filter(user__gender=preference.preferred_gender)


    # Preferred religion
    if preference.religion != 'Any':
        profiles = profiles.filter(religion=preference.religion)


    # Preferred marital status
    if preference.marital_status != 'Any':
        profiles = profiles.filter(marital_status=preference.marital_status)


    # Preferred city
    if preference.city:
        profiles = profiles.filter(city__icontains=preference.city)


    # Exclude users blocked in either direction
    blocked_by_me = BlockedUser.objects.filter(blocker=request.user).values_list('blocked_id', flat=True)


    blocked_me = BlockedUser.objects.filter(blocked=request.user).values_list('blocker_id', flat=True)


    profiles = profiles.exclude(user_id__in=blocked_by_me).exclude(user_id__in=blocked_me)


    return render(request,'matches.html',{'profiles': profiles,'preference': preference})