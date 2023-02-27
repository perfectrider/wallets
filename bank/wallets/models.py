from django.db import models

class BankUser(models.Model):
    pass

class Wallet(models.Model):
    name = models.CharField()
    type = models.Choices()
    currency = models.Choices()
    balance = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    sender = models.ForeignKey(BankUser)
    reciever = models.ForeignKey(BankUser)
    transfer_amount = models.IntegerField()
    comission = models.IntegerField()
    status = models.Choices()
    timestamp = models.DateTimeField(auto_now_add=True)