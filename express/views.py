from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from .models import Profile, Message, Comment
from django.http import JsonResponse, HttpResponse

def home(request):
    return render(request, 'home.html', {})

def not_authenticated(user):
    return not user.is_authenticated

@user_passes_test(not_authenticated, login_url='dashboard')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = Profile(user=user)
            profile.image = "default.png"
            profile.save()
            user.save()
            raw_password = form.cleaned_data.get('password')
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@user_passes_test(not_authenticated, login_url='dashboard')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid login. Username or Password is Incorrect.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    messages = Message.objects.filter(user=request.user).order_by('-timestamp')
    if request.method == 'POST':
        bio = request.POST.get('bio', None)
        if bio is not None:
            profile.bio = bio
            profile.save()
            return redirect('dashboard')
        message = request.POST.get('message', None)
        if message is not None:
            m = Message(user=profile.user, message=message)
            m.save()
            return redirect('dashboard')
        if 'image' in request.FILES:
            image = request.FILES['image']
            profile.image = image
            profile.save()
        context = {'profile': profile, 'messages': messages, 'can_delete': True}
        return render(request, 'dashboard.html', context)
    else:
        context = {'profile': profile, 'messages': messages, 'can_delete': True}
        return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    response = redirect('home')
    response.delete_cookie('sessionid')
    return response

@login_required
def newsfeed(request):
    messages = Message.objects.select_related('user').all().order_by('-timestamp')
    context = {'messages': messages}
    return render(request, 'newsfeed.html', context)

@login_required
def view_page(request):
    if not request.user.is_authenticated:
        return redirect('home')
    exclude_filter = []
    if not request.user.is_authenticated:
        exclude_filter = ["dashboard", "newsfeed"]
    return render(request, 'page.html', {'exclude_filter': exclude_filter})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return HttpResponse(status=204)

@login_required
def add_comment(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        comment = Comment(message=message, user=request.user, comment=request.POST.get('comment'))
        comment.save()
        comment_data = {
            'id': comment.id,
            'user': comment.user.username,
            'comment': comment.comment,
            'timestamp': comment.timestamp.strftime("%B %d, %Y %I:%M %p"),
            'user_id': comment.user.id,
            'user_image_url': comment.user.profile.image.url,
            'current_user_id': request.user.id
        }
        return JsonResponse(comment_data)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return JsonResponse({'deleted': True})