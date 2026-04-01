from django.contrib import admin
from .models import Medicine, Batch, Transaction


# ==========================
# Medicine Admin
# ==========================
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'prescription_required')
    search_fields = ('name',)


# ==========================
# Batch Admin
# ==========================
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'medicine',
        'batch_number',
        'expiration_date',
        'quantity',
        'price',
    )

    list_filter = (
        'expiration_date',
    )

    search_fields = (
        'medicine__name',
        'batch_number',
    )


# ==========================
# Transaction Admin
# ==========================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'batch',
        'quantity',
        'pharmacist',
        'timestamp',
        'hash',
    )

    list_filter = (
        'timestamp',
    )

    search_fields = (
        'batch__medicine__name',
        'pharmacist',
    )