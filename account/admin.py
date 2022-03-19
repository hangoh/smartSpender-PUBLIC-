from django.contrib import admin
from account.models import Account 
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display=['email','username','is_admin','is_active','date_joined','last_login']
    list_filter = ['email','username','is_active']
    search_fields = ['email','username']

admin.site.register(Account, AccountAdmin)
    
