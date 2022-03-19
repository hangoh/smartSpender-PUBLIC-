from distutils.text_file import TextFile
from django.db import models
from django.forms import DateField, DateTimeField
from sqlalchemy import false
from tables import Description
from account.models import Account
# Create your models here.

class Expenses(models.Model):
    owner = models.ForeignKey("Account", on_delete=models.CASCADE)
    caterogy = models.CharField(max_length=256, null=False, blank = False)
    amount = models.DecimalField( max_digits=19, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    dateUsage = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.category)