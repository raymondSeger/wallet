from django.contrib import admin

# Register your models here.
from test_wallet_app.models import Wallet, User, Transaction_Data

admin.site.register(User)
admin.site.register(Transaction_Data)

class Transaction_Data_Inline(admin.StackedInline):
    model = Transaction_Data
    extra = 0

class WalletAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            "the_id",
            "wallet_name",
            "enabled_status",
            "enabled_at",
            "disabled_at"
        ]}),
    ]
    inlines = [Transaction_Data_Inline]

admin.site.register(Wallet, WalletAdmin)