import decimal
from django.contrib.auth.models import User
from django.db import models, transaction


class Wallet(models.Model):
    '''Customer wallet. Each customer cannot create more than 5 wallets'''

    CARD_TYPE_CHOICES = [
        ('Visa', 'Visa'),
        ('MasterCard', 'Master Card'),
    ]

    CURRENCY_CHOICES = [
        ('RUB', 'Ruble'),
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
    ]

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='wallets')
    name = models.SlugField(max_length=8)
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
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=1, null=False)
    status = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def make_transaction(cls, sender, receiver, transfer_amount):
        if sender.balance < transfer_amount:
            raise (ValueError('Not enough money on the current wallet!'))
        if sender.balance == receiver.balance:
            raise (ValueError('Receiver wallet is a sender wallet!'))

        with transaction.atomic():
            if sender.owner == receiver.owner:
                sender.balance -= transfer_amount
            else:
                sender.balance -= transfer_amount * decimal.Decimal(1.1)
            sender.save()
            receiver.balance += transfer_amount
            receiver.save()
            tran = cls.objects.create(sender=sender,
                                       receiver=receiver,
                                       transfer_amount=transfer_amount,
                                       )
        return tran, sender, receiver
