from django.contrib import admin
from .models import Event
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    # Keep readonly so the automatic ID doesn't confuse the form
    readonly_fields = ('id',) 
    
    list_display = ('thumbnail', 'title', 'organizer', 'capacity_status', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'organizer')
    
    # 4. FIXED: Updated to use the new ImageField attribute
    def thumbnail(self, obj):
        if obj.image: # Safety check in case no image was uploaded
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "No Image"
    thumbnail.short_description = 'Preview'

    def capacity_status(self, obj):
        # Prevent division by zero if capacity is 0
        if obj.capacity <= 0: return "0/0"
        
        percent = (obj.signed_up_count / obj.capacity) * 100
        color = "green" if percent < 80 else "orange" if percent < 100 else "red"
        return format_html(
            '<b style="color: {};">{}/{} ({}%)</b>',
            color, obj.signed_up_count, obj.capacity, int(percent)
        )
    capacity_status.short_description = 'Fill Rate'