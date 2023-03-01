from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Customer(models.Model):
    '''User ob bank application'''

    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Wallet(models.Model):
    '''Customer wallet. Each customer cannot create more than 5 wallets'''

    CARD_TYPE_CHOICES = [
        ( 'Visa', 'Visa'),
        ('MasterCard', 'Master Card')
    ]

    CURRENCY_CHOICES = [
        ('RUB', 'Ruble'),
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),

    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='wallets')
    name = models.CharField(max_length=8)
    type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'


class Transaction(models.Model):
    '''Describes departure and destination points, amount of transaction and some details.'''

    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='from_wallet')
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='to_wallet')
    transfer_amount = models.DecimalField(max_digits=12, decimal_places=2)
    # status = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)