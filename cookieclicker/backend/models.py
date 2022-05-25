from django.db import models
from django.contrib.auth.models import User


# Game save data, one user = one save (one to one)
# be one to many, many to one, many to many
class Core(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE) # delete all raw
    coins = models.IntegerField(default=0)
    click_power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)

    def click(self, commit=True):
        self.coins += self.click_power
        is_levelupdated = self.is_levelup()
        if is_levelupdated:
            self.level += 1
        if commit:
            self.save()

        return is_levelupdated

    def is_levelup(self):
        return self.coins > (self.level**2+1)*100*(self.level+1)


class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    power = models.IntegerField(default=1)
