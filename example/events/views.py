from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Event, Ticket
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail

def event_feed(request):
    if not request.user.is_authenticated:
        return redirect('login')
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/feed.html', {'events': events})

# ADD THIS NEW FUNCTION:
from .utils import render_to_pdf

def register_event(request, event_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to join events!")
        return redirect('signup')

    event = get_object_or_404(Event, id=event_id)
    
    # Check if already registered
    ticket = Ticket.objects.filter(user=request.user, event=event).first()
    
    if not ticket:
        if event.signed_up_count < event.capacity:
            # Create Ticket Record
            ticket = Ticket.objects.create(
                user=request.user,
                event=event,
                is_paid=(event.event_type == 'FREE') # Mark as paid if free
            )
            
            event.signed_up_count += 1
            event.save()
            messages.success(request, f"Successfully joined {event.title}!")
        else:
            messages.error(request, "Could not complete registration. The event might be full.")
            return redirect('event_detail', event_id=event.id)
    
    # Generate PDF (for new or existing registration)
    base_url = f"{request.scheme}://{request.get_host()}"
    verify_url = f"{base_url}/verify/{ticket.ticket_id}/"
    
    response = render_to_pdf('events/ticket_pdf.html', {
        'ticket': ticket,
        'verify_url': verify_url
    })
    
    if response:
        filename = f"Ticket_{event.title.replace(' ', '_')}_{str(ticket.ticket_id)[:8]}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
            
    messages.error(request, "Could not complete registration or generate ticket.")
    return redirect('event_detail', event_id=event.id)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
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
    if request.user.is_authenticated:
        return redirect('home')
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
    event = get_object_or_404(Event, id=event_id)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Ticket.objects.filter(user=request.user, event=event).exists()
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered
    })

import json

def calendar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    user_tickets = Ticket.objects.filter(user=request.user).select_related('event')
    
    event_list = []
    for ticket in user_tickets:
        event = ticket.event
        event_list.append({
            'title': event.title,
            'start': event.event_date.isoformat(), 
            'url': f'/event/{event.id}/',
            'backgroundColor': '#064e3b',
        })
    
    return render(request, 'events/calendar.html', {'events_json': json.dumps(event_list)})

def verify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(request, 'events/verify_result.html', {'ticket': ticket})

def my_registrations(request):
    tickets = Ticket.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_registrations.html', {'tickets': tickets})

from .forms import EventForm

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Calculate stats
    total_tickets = Ticket.objects.filter(user=request.user).count()
    # Assuming we might have an 'organized_events' relationship or we filter events by organizers if added later
    # For now, just user info
    
    return render(request, 'events/profile.html', {
        'user': request.user,
        'total_tickets': total_tickets
    })

def add_event_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create an event.")
        return redirect('login')
        
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Set the organizer to the logged-in user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
        
    return render(request, 'events/add_event.html', {'form': form})
