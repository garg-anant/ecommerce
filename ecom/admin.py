from django.contrib import admin

# Register yourfrom django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProfileUser, LedgerTable 

# admin.site.register(User)
admin.site.register(LedgerTable)
admin.site.register(ProfileUser)
