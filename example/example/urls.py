from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from events.views import event_feed, register_event, signup_view, login_view, event_detail, calendar_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_feed, name='home'),
    path('register/<str:event_id>/', register_event, name='register_event'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', login_view, name='login'),
    path('event/<str:event_id>/', event_detail, name='event_detail'),
    path('calendar/', calendar_view, name='calendar'), # 2. Add this line
]

# Only add this ONCE at the very bottom
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)