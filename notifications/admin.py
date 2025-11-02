from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','product','title','message','type','sent_at','is_read')
    list_display_links = ('user','product')
    search_fields = ('user','product','title','sent_at')
    list_per_page = 25
admin.site.register(Notification, NotificationAdmin)