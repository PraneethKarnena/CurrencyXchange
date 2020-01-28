from django.db import models
from django.contrib.auth.models import User


class PictureModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    file = models.FileField(upload_to='profile-pictures/', null=False, blank=False)

    def __str__(self):
        return f'{self.user.email} - {self.file.name}'


class WalletModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    money = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user.email} - {self.money}'


class CurrencyConversionModel(models.Model):

    from_currency = models.CharField(max_length=3, null=False, blank=False)
    to_currency = models.CharField(max_length=3, null=False, blank=False)

    from_amount = models.FloatField(default=1.00)
    to_amount = models.FloatField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['from_currency', 'to_currency',]

    def __str__(self):
        return f'{self.from_currency} to {self.to_currency}: {self.to_amount}'