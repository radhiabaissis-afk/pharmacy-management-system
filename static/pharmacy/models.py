from django.db import models
from django.utils import timezone
from datetime import timedelta
import hashlib

# ----------------------------
# Alert Settings
LOW_STOCK_THRESHOLD = 10
EXPIRY_ALERT_DAYS = 30
# ----------------------------


# ============================
# Medicine Model
# ============================
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    prescription_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ============================
# Batch Model (Professional Structure)
# ============================
class Batch(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='batches'
    )
    batch_number = models.CharField(max_length=50)
    expiration_date = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} - Batch: {self.batch_number}"

    def is_expiring_soon(self):
        return self.expiration_date <= timezone.now().date() + timedelta(days=EXPIRY_ALERT_DAYS)

    def is_low_stock(self):
        return self.quantity <= LOW_STOCK_THRESHOLD


# ============================
# Transaction Model
# ============================
class Transaction(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    pharmacist = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    prescription_id = models.CharField(max_length=50, blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):

        # Check stock availability
        if self.batch.quantity < self.quantity:
            raise ValueError("Not enough stock available!")

        # Reduce stock from batch
        self.batch.quantity -= self.quantity
        self.batch.save()

        # First save (to get timestamp)
        super().save(*args, **kwargs)

        # Generate transaction hash (Blockchain-style integrity)
        data = f"{self.batch.id}{self.quantity}{self.pharmacist}{self.timestamp}{self.prescription_id}"
        self.hash = hashlib.sha256(data.encode()).hexdigest()

        # Update only hash field
        super().save(update_fields=['hash'])

    def __str__(self):
        return f"Transaction: {self.batch.medicine.name} - Qty: {self.quantity}"
    