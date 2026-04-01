from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Medicine, Transaction


# =============================
# Dashboard
# =============================
def dashboard(request):
    total_medicines = Medicine.objects.count()
    total_transactions = Transaction.objects.count()

    total_revenue = 0
    transactions = Transaction.objects.all()

    for t in transactions:
        total_revenue += t.medicine.price * t.quantity

    context = {
        'total_medicines': total_medicines,
        'total_transactions': total_transactions,
        'total_revenue': total_revenue,
    }

    return render(request, 'pharmacy/dashboard.html', context)


# =============================
# Medicine List
# =============================
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/medicine_list.html', {'medicines': medicines})


# =============================
# Sell Medicine
# =============================
def sell_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        pharmacist = request.POST.get('pharmacist')
        prescription_id = request.POST.get('prescription_id')

        if quantity > medicine.quantity:
            messages.error(request, "Not enough stock!")
            return redirect('sell_medicine', pk=pk)

        Transaction.objects.create(
            medicine=medicine,
            quantity=quantity,
            pharmacist=pharmacist,
            prescription_id=prescription_id
        )

        messages.success(request, "Sale completed successfully!")
        return redirect('medicine_list')

    return render(request, 'pharmacy/sell_medicine.html', {'medicine': medicine})


# =============================
# Transaction List
# =============================
def transaction_list(request):
    transactions = Transaction.objects.order_by('-timestamp')
    return render(request, 'pharmacy/transaction_list.html', {
        'transactions': transactions
    })