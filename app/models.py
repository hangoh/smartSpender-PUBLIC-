from django.db import models
from account.models import Account
# Create your models here.

class Expenses(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False, blank = False)
    category = models.CharField(max_length=256, null=False, blank = False)
    amount = models.DecimalField(decimal_places=2, max_digits=20,null=False, blank = False)
    description = models.TextField(null=True, blank=True)
    dateUsage = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.title)