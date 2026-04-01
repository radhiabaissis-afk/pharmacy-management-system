from django.shortcuts import render, get_object_or_404, redirect
from .models import Batch, Transaction
from django.utils import timezone


# 🟢 Dashboard
def dashboard(request):
    return render(request, 'pharmacy/dashboard.html')


# 🟢 عرض الأدوية
def medicine_list(request):
    batches = Batch.objects.select_related('medicine')
    return render(request, 'pharmacy/medicine_list.html', {
        'batches': batches
    })


# 🟢 بيع دواء
def sell_medicine(request, pk):
    batch = get_object_or_404(Batch, pk=pk)

    if batch.quantity > 0:
        batch.quantity -= 1
        batch.save()

        Transaction.objects.create(
            batch=batch,
            quantity_sold=1,
            date=timezone.now()
        )

    return redirect('medicine_list')


# 🟢 عرض المعاملات
def transaction_list(request):
    transactions = Transaction.objects.select_related('batch')
    return render(request, 'pharmacy/transaction_list.html', {
        'transactions': transactions
    })