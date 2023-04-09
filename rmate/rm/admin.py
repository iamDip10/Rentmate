from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Residant)
admin.site.register(Pro_owner)
admin.site.register(Complain)
admin.site.register(ResRent)
admin.site.register(Notifications)
admin.site.register(activity)
admin.site.register(otherActivity)
