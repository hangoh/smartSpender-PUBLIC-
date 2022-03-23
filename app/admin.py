from django.contrib import admin
from app.models import *
# Register your models here.

class ExpensesAdmin(admin.ModelAdmin):
    list_display=['owner','title','amount','category']
    list_filter = ['owner','category']
    search_fields = ['owner','category']

admin.site.register(Expenses,ExpensesAdmin)