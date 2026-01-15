from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Ticket
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail

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

def event_detail(request, event_id):
    # Fetch the specific event or return 404 if it doesn't exist
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def event_detail(request, event_id):
    # Fetch the event from MongoDB by ID
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

import json

def calendar_view(request):
    events = Event.objects.all()
    event_list = []
    
    for event in events:
        event_list.append({
            'title': event.title,
            # Use the new event_date field here
            'start': event.event_date.isoformat(), 
            'url': f'/event/{event.id}/',
            'backgroundColor': '#5865f2',
        })
    
    return render(request, 'events/calendar.html', {'events_json': event_list})

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if not request.user.is_authenticated:
        messages.error(request, "Please login to register.")
        return redirect('login')

    # Logic: Check if it's a Paid Event
    if event.event_type == 'PAID':
        # Store event_id in session so the payment page knows what we're buying
        request.session['pending_event_id'] = str(event.id)
        return redirect('payment_page')
    
    # Logic: Free Event Flow
    if event.signed_up_count < event.capacity:
        event.signed_up_count += 1
        event.save()
        messages.success(request, f"You are registered for {event.title}!")
    else:
        messages.error(request, "This event is full.")
        
    return redirect('home')

def payment_page(request):
    event_id = request.session.get('pending_event_id')
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/payment.html', {'event': event})

def event_signup_form(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    
    if request.method == 'POST':
        # Logic: If Paid, go to payment. If Free, create ticket now.
        if event.event_type == 'PAID':
            request.session['pending_event_id'] = str(event.id)
            return redirect('payment_page')
        else:
            # Create Ticket for Free Event
            Ticket.objects.create(user=user, event=event, is_paid=True)
            event.signed_up_count += 1
            event.save()
            
            # Send Mock Email (Console)
            print(f"Sending Ticket to {user.email}...") 
            
            messages.success(request, "Ticket generated and sent to email!")
            return redirect('my_registrations')

    return render(request, 'events/signup_form.html', {
        'event': event,
        'user': user
    })

def my_registrations(request):
    # Fetch all tickets belonging to the logged-in user
    tickets = Ticket.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_registrations.html', {'tickets': tickets})


def event_signup_form(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    
    if request.method == 'POST':
        # Logic: If Paid, go to payment. If Free, create ticket now.
        if event.event_type == 'PAID':
            request.session['pending_event_id'] = str(event.id)
            return redirect('payment_page')
        else:
            # Create Ticket for Free Event
            Ticket.objects.create(user=user, event=event, is_paid=True)
            event.signed_up_count += 1
            event.save()
            
            # Send Mock Email (Console)
            print(f"Sending Ticket to {user.email}...") 
            
            messages.success(request, "Ticket generated and sent to email!")
            return redirect('my_registrations')

    return render(request, 'events/signup_form.html', {
        'event': event,
        'user': user
    })