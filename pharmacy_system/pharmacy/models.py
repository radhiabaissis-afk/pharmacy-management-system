from django.db import models
from django.utils import timezone
from datetime import timedelta
import hashlib

# ----------------------------
# إعدادات التنبيهات
LOW_STOCK_THRESHOLD = 10
EXPIRY_ALERT_DAYS = 30
# ----------------------------

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    batch_number = models.CharField(max_length=50)
    expiration_date = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prescription_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Batch: {self.batch_number}"

    def is_expiring_soon(self):
        return self.expiration_date <= timezone.now().date() + timedelta(days=EXPIRY_ALERT_DAYS)

    def is_low_stock(self):
        return self.quantity <= LOW_STOCK_THRESHOLD


class Transaction(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    pharmacist = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    prescription_id = models.CharField(max_length=50, blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        # التحقق من توفر الكمية
        if self.medicine.quantity < self.quantity:
            raise ValueError("Not enough stock available!")

        # إنقاص الكمية من المخزون
        self.medicine.quantity -= self.quantity
        self.medicine.save()

        # حفظ أولي للحصول على timestamp
        super().save(*args, **kwargs)

        # إنشاء hash
        data = f"{self.medicine.id}{self.quantity}{self.pharmacist}{self.timestamp}{self.prescription_id}"
        self.hash = hashlib.sha256(data.encode()).hexdigest()

        # تحديث الحقل hash فقط
        super().save(update_fields=['hash'])

    def __str__(self):
        return f"Transaction: {self.medicine.name} - Qty: {self.quantity} - By: {self.pharmacist}"