from django.contrib import admin
from .models import Medicine, Batch, Transaction

admin.site.register(Medicine)
admin.site.register(Batch)
admin.site.register(Transaction)