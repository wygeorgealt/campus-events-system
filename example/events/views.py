from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


# Keep your existing event_feed view...
def event_feed(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/feed.html', {'events': events})

# ADD THIS NEW FUNCTION:
def register_event(request, event_id):
    # Security check: If not logged in, send them to signup
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to join events!")
        return redirect('signup')

    if request.method == "POST":
        event = get_object_or_404(Event, id=event_id)
        if event.signed_up_count < event.capacity:
            event.signed_up_count += 1
            event.save()
            messages.success(request, f"Successfully joined {event.title}!")
    
    return redirect('home')


def signup_view(request):
    if request.method == "POST":
        uname = request.POST['username']
        email = request.POST['email']
        
        # Check if Username or Email is taken
        if User.objects.filter(username=uname).exists():
            messages.error(request, "This username is already taken.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('signup')
            
        u = User.objects.create_user(uname, email, request.POST['password'])
        u.first_name, u.last_name = request.POST['f_name'], request.POST['l_name']
        u.save()
        login(request, u)
        return redirect('home')
    return render(request, 'events/signup.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'events/login.html')