from django.contrib import admin

from .models import GPUInfo, Server

# Register your models here.
admin.site.register(Server)
admin.site.register(GPUInfo)
