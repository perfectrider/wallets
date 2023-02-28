from django.contrib import admin
from .models import *

# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'created_on')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'transfer_amount', 'timestamp')


# admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)


