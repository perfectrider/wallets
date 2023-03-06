from rest_framework import serializers
from wallets.models import Wallet, Transaction
from django.contrib.auth.models import User


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']
        lookup_field = 'name'


class UserSerializer(serializers.ModelSerializer):
    wallets = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['username', 'wallets']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.CharField()
    commission = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    def validate(self, data):
        try:
            data['sender'] = Wallet.objects.get(name=data['sender'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "No such account from serializer")
        return data

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount', 'commission', 'status', 'timestamp']