from django.shortcuts import render,get_object_or_404,redirect
from user_profile.models import MatrimonialProfile
from django.contrib.auth.decorators import login_required
from connections.models import Interest
from django.db.models import Q
from connections.models import BlockedUser
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    profile = MatrimonialProfile.objects.filter(user=request.user).first()
    total_profiles = MatrimonialProfile.objects.filter(is_active=True).exclude(user=request.user).count()
    received_interests = Interest.objects.filter(receiver=request.user).count()
    sent_interests = Interest.objects.filter(sender=request.user).count()
    accepted_interests = Interest.objects.filter(Q(sender=request.user) | Q(receiver=request.user),status='Accepted').count()
    context = {
        'profile':profile,
        'total_profiles':total_profiles,
        'received_interests':received_interests,
        'sent_interests':sent_interests,
        'accepted_interests':accepted_interests
    }
    return render(request,'home.html',context)

@login_required
def browse_profiles(request):
    profiles = MatrimonialProfile.objects.filter(is_active=True).exclude(user=request.user).select_related('user')
    blocked_by_me = BlockedUser.objects.filter(blocker = request.user).values_list('blocked_id',flat=True)
    blocked_me = BlockedUser.objects.filter(blocked = request.user).values_list('blocked_id',flat=True)
    profiles = profiles.exclude(user_id__in = blocked_by_me).exclude(user_id__in = blocked_me)
    gender = request.GET.get('gender')
    religion = request.GET.get('religion')
    city = request.GET.get('city')
    marital_status = request.GET.get('marital_status')
    search = request.GET.get('search')
    if gender:
        profiles = profiles.filter(user__gender=gender)
    if religion:
        profiles = profiles.filter(religion=religion)
    if city:
        profiles = profiles.filter(city__icontains = city)
    if marital_status:
        profiles = profiles.filter(marital_status=marital_status)
    if search:
        profiles = profiles.filter(user__first_name__icontains = search) | profiles.filter(user__last_name__icontains = search)
    return render(request,'browse_profiles.html',{'profiles':profiles})

@login_required
def profile_detail(request,pk):
    profile = get_object_or_404(MatrimonialProfile.objects.select_related('user'),id=pk,is_active=True)
    is_blocked = BlockedUser.objects.filter(
        Q(blocker=request.user,blocked=profile.user) |
        Q(blocker=profile.user,blocked=request.user)
    ).exists()
    if is_blocked:
        messages.error(request,"You cannot view this profile.")
        return redirect('browse_profiles')
    return render(request,'profile_detail.html',{'profile':profile})