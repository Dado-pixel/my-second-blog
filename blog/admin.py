from django.contrib import admin
from .models import Post, User, IP


class IPAdmin(admin.ModelAdmin):
    list_display = ['User', 'entr_date', 'ip_address']
    class Meta:
        model = IP

admin.site.register(Post)
admin.site.register(IP, IPAdmin)
