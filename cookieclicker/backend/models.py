from django.db import models
from django.contrib.auth.models import User


# Game save data, one user = one save (one to one)
# be one to many, many to one, many to many
class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE) # delete all raw
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)

