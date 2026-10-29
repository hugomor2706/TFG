from django.contrib import admin
from .models import User, Card, Door, Permission, Device, AccessLog


admin.site.register(User)
admin.site.register(Card)
admin.site.register(Door)
admin.site.register(Permission)
admin.site.register(Device)
admin.site.register(AccessLog)