from django.shortcuts import render, redirect
from .models import Profile, User, Skill, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .form import CustomUserCreationForm, EditProfileForm, AddSkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles, profiles_pagination

def profiles(request):
    profiles, search_query = search_profiles(request)
    per_page=2

    profiles, custom_range = profiles_pagination(request, profiles, per_page)

    context = {'profiles':profiles, 'search_query':search_query, 
               'custom_range':custom_range }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # get skills with description by exlcuding
    top_skills = profile.skill_set.exclude(description__exact='')
    # get skills with no description
    other_skills = profile.skill_set.filter(description='')
    # get projets
    projects = profile.project_set.all()

    context = {'profile':profile, 'top_skills':top_skills, 
               "other_skills":other_skills, 'projects':projects }
    return render(request, 'users/user_profile.html', context)


def login_user(request):
    page = 'login'
    context = {'page': page}
    # if user is already logged in, redirect
    if request.user.is_authenticated:
         return redirect('profiles') 

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        # check if user exists
        try:
            user = User.objects.get(username=username)    
        except:
            messages.error(request, 'Username does not exist')

        # check user by matching with password and login
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
                login(request, user)
                messages.info(request, 'Logged in')    
                return redirect(request.GET['next'] if request.GET else 'user_account')
        else:
            messages.error(request, 'username or password is incorrect')
    return render(request, 'users/login_register.html', context)


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page':page, 'form':form}

    # register user 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created')
            login(request, user)
            return redirect('edit_account')
        
        messages.error(request, 'Registration failed for some reason')
        return render(request,'users/login_register.html', {'form':form, 'page':page})

    return render(request, 'users/login_register.html', context)


def logout_user(request):
     print(request)
     logout(request)
     messages.info(request, 'Logged out')
     return redirect('login')


# user account page
@login_required(login_url='login')
def user_account(request):
    # pass current user profile from request obj
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills':skills, 'projects':projects}
    return render(request,'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    # to edit logged in user, get user.profile from request
    profile = request.user.profile
    form = EditProfileForm(instance=profile)
    context = {'form': form}
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = profile.username.lower()
            profile.save()
            messages.success(request, 'Account edited')
            return redirect('user_account')
    
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def add_skill(request):
    form = AddSkillForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        form = AddSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added')
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = AddSkillForm(instance = skill)
    context = {'form': form}
    if request.method == 'POST':
        form = AddSkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('user_account')

    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    print('inside delete skill view')
    if request.method == 'POST':
        skill.delete()
        print('deleted')
        # messages.success(request, 'Skill deleted')
        return redirect('user_account')
    context = {'object':skill}
    
    return render(request, 'projects/delete_object.html', context)


@login_required(login_url='login')
def inbox(request):
    # get profile, and then profiles messages
    profile = request.user.profile
    inbox_items = profile.messages.all()
    unread_count = inbox_items.filter(is_read=False).count()
    context = {'inbox':inbox_items, 'unread_count':unread_count}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    msg = profile.messages.get(id=pk)
    # this way anyone can see message by passing pk
    # msg = Message.objects.get(id=pk) #dont use this
    if not msg.is_read: 
        msg.is_read = True
        msg.save()
    context = {'msg':msg}

    return render(request, 'users/message.html', context)

def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    context = {'form':form, 'recipient':recipient}

    # check if user is logged in and assign to sender
    try:
        sender = request.user.profile
    except:
        sender=None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            message.sender = sender
            
            # if a user is logged in, pass name and email
            if sender:
                message.name = sender.name
                message.email = sender.email
            form.save()
            messages.success(request, 'Message sent!')
            return redirect('user_profile', pk=pk)
    return render(request, 'users/send_message.html', context)