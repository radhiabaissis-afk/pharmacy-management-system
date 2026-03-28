from django.contrib import admin
from .models import Medicine, Transaction

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'batch_number',
        'expiration_date',
        'quantity',
        'price',
        'prescription_required',
        'low_stock',
        'expiring_soon'
    )
    list_filter = ('expiration_date', 'prescription_required')
    search_fields = ('name', 'batch_number')

    def low_stock(self, obj):
        return obj.is_low_stock()
    low_stock.boolean = True
    low_stock.short_description = 'Low Stock?'

    def expiring_soon(self, obj):
        return obj.is_expiring_soon()
    expiring_soon.boolean = True
    expiring_soon.short_description = 'Expiring Soon?'
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity', 'pharmacist', 'timestamp', 'prescription_id', 'hash')
    search_fields = ('medicine__name', 'pharmacist', 'prescription_id')
    readonly_fields = ('hash', 'timestamp')