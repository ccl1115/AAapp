from django.contrib import admin
from AAapp.AA.models import AccountInfo, Expense

class AccountInfoAdmin(admin.ModelAdmin):
    pass

class ExpenseAdmin(admin.ModelAdmin):
    pass

admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(Expense, ExpenseAdmin)
