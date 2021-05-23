from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def my_profile_view(request):
    # This gets profile of user that is logged in
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True


    context = {'profile': profile, 'form': form, 'confirm': confirm}
    return render(request, 'profiles/myprofile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)

    qs = Relationship.objects.invitations_received(profile)
    # This changes Testuser6-23-05-2021-John-18-05-2021-send to Testuser6-23-05-2021
    result = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {'qs': result, 'is_empty': is_empty}
    return render(request, 'profiles/my_invites.html', context)

def accept_invitation(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

def reject_invitation(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

def invites_profiles_list_view(request):
    user=request.user

    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}
    return render(request, 'profiles/to_invite_list.html', context)

def profiles_list_view(request):
    user=request.user

    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}
    return render(request, 'profiles/profile_list.html', context)

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # The 'qs' below is used for template usage. If line below isn't used then you would have to use object_list in for loop in profile_list.html instead of qs
    #context_object_name = 'qs'

    # To override Profile.objects.all()

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    # Below is to add additional content to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Secure way of getting user while using class based functions
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        # Below is like using context = {'profile': profile}
        #context['profile'] = profile
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

def send_invitation(request):
    if request.method == 'POST':
        # Below gets the promary key from profile_list.html that has <input type="hidden" name="profile_pk" value="{{ obj.pk }}"> 
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

def remove_from_friends(request):
    if request.method == 'POST':
        # Below gets the promary key from profile_list.html that has <input type="hidden" name="profile_pk" value="{{ obj.pk }}"> 
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender)
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')