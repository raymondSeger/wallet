from django.db import models
from django.db.models import DecimalField
from django.utils.timezone import now

class User(models.Model):
    the_id          = models.TextField(verbose_name="Customer ID", default='', blank=False, null=True, )
    auth_token      = models.TextField(verbose_name="Auth Token", default='', blank=False, null=True, )
    name            = models.CharField(verbose_name="Name", max_length=255, default='', blank=False, null=True, )
    email           = models.CharField(verbose_name="Email", max_length=255, default='', blank=False, null=True, )
    hashed_password = models.TextField(verbose_name="Hashed Password", default='', blank=False, null=True, )
    user_wallet     = models.ManyToManyField('Wallet', related_name="user_wallet", verbose_name="User's Wallet", blank=True)
    created         = models.DateTimeField(default=now)
    modified        = models.DateTimeField(editable=True, auto_now=True)

    def __str__(self):
        return "User %s %s" % (self.name, self.email,)

    class Meta:
        verbose_name        = "User"
        verbose_name_plural = "Users"

class Wallet(models.Model):
    the_id          = models.TextField(verbose_name="Wallet ID", default='', blank=False, null=True, )
    wallet_name     = models.TextField(verbose_name="Wallet Name", default='', blank=True, null=True, )
    enabled_status  = models.BooleanField(verbose_name="Enabled Status", default=True)
    enabled_at      = models.DateTimeField(verbose_name="Enabled At", editable=True, auto_now=False, blank=True, null=True, )
    disabled_at     = models.DateTimeField(verbose_name="Disabled At", editable=True, auto_now=False, blank=True, null=True, )
    created         = models.DateTimeField(default=now)
    modified        = models.DateTimeField(editable=True, auto_now=True)

    def __str__(self):
        return "Wallet %s %s" % (self.id, self.the_id,)

    class Meta:
        verbose_name        = "Wallet"
        verbose_name_plural = "Wallets"

class Transaction_Data(models.Model):
    reference_id        = models.TextField(verbose_name="Deposited By", unique=True, default=None, max_length=255, blank=False, null=False, )
    transaction_data    = models.ForeignKey(Wallet, default=None, on_delete=models.CASCADE)
    amount              = DecimalField(verbose_name="Amount", max_digits=40, decimal_places=2, default=0)
    deposited_by        = models.CharField(verbose_name="Deposited By", max_length=255, default='', blank=True, null=True, )
    deposited_at        = models.DateTimeField(verbose_name="Deposited At", editable=True, blank=True, null=True, )
    withdrawn_by        = models.CharField(verbose_name="Withdrawn By", max_length=255, default='', blank=True, null=True, )
    withdrawn_at        = models.DateTimeField(verbose_name="Withdrawn At", editable=True, blank=True, null=True, )
    created             = models.DateTimeField(default=now)
    modified            = models.DateTimeField(editable=True, auto_now=True)

    def __str__(self):
        return "Transaction Data #%s" % (self.id)

    class Meta:
        verbose_name        = "Transaction Data"
        verbose_name_plural = "Transaction Data"

