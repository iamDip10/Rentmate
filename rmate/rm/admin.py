from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Residant)
admin.site.register(Complain)
admin.site.register(Pro_owner)
admin.site.register(ResRent)
admin.site.register(Notifications)
admin.site.register(activity)
admin.site.register(otherActivity)
admin.site.register(rating)
admin.site.register(apartment)
admin.site.register(advertisment)
admin.site.register(waitforapproval)
admin.site.register(report)