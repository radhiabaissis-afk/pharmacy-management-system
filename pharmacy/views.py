from .forms import MedicineForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medicine, Batch, Transaction


# =============================
# Dashboard
# =============================
from django.db.models import Sum
from .models import Medicine, Batch, Transaction

def dashboard(request):
    total_medicines = Medicine.objects.count()
    total_batches = Batch.objects.count()

    total_stock = Batch.objects.aggregate(total=Sum('quantity'))['total'] or 0

    total_revenue = 0
    transactions = Transaction.objects.all()
    for t in transactions:
        total_revenue += t.batch.price * t.quantity

    # 🚨 Low Stock (أقل من 5)
    low_stock_batches = Batch.objects.filter(quantity__lt=5)
    low_stock_count = low_stock_batches.count()

    context = {
        'total_medicines': total_medicines,
        'total_batches': total_batches,
        'total_stock': total_stock,
        'total_revenue': total_revenue,
        'low_stock_count': low_stock_count,
        'low_stock_batches': low_stock_batches,
    }

    return render(request, 'pharmacy/dashboard.html', context)
# =============================
# Medicine List
# ====

def medicine_list(request):
    query = request.GET.get('q')

    batches = Batch.objects.select_related('medicine')

    if query:
        batches = batches.filter(medicine__name__icontains=query)

    return render(request, 'pharmacy/medicine_list.html', {
        'batches': batches,
        'query': query
    })

def add_batch(request):
    medicines = Medicine.objects.all()

    if request.method == "POST":
        medicine_id = request.POST.get('medicine')
        batch_number = request.POST.get('batch_number')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        expiration_date = request.POST.get('expiration_date')

        medicine = Medicine.objects.get(id=medicine_id)

        Batch.objects.create(
            medicine=medicine,
            batch_number=batch_number,
            quantity=quantity,
            price=price,
            expiration_date=expiration_date
        )

        return redirect('medicine_list')

    return render(request, 'pharmacy/add_batch.html', {
        'medicines': medicines
    })
# =============================
# Sell Medicine
# =============================
from django.shortcuts import get_object_or_404

def sell_medicine(request, pk):
    batch = get_object_or_404(Batch, pk=pk)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        pharmacist = request.POST.get('pharmacist')
        prescription_id = request.POST.get('prescription_id')

        if quantity > batch.quantity:
            messages.error(request, "Not enough stock!")
            return redirect('sell_medicine', pk=pk)

        # إنشاء عملية البيع (سيقوم موديل Transaction بإنقاص الكمية تلقائيًا)
        Transaction.objects.create(
            batch=batch,
            quantity=quantity,
            pharmacist=pharmacist,
            prescription_id=prescription_id
        )

        messages.success(request, "Sale completed successfully!")
        return redirect('medicine_list')

    return render(request, 'pharmacy/sell_medicine.html', {
        'batch': batch
    })

# =============================
# Transaction List
# =============================
def transaction_list(request):
    transactions = Transaction.objects.order_by('-timestamp')
    return render(request, 'pharmacy/transaction_list.html', {
        'transactions': transactions
    })
def home(request):
    return render(request, 'pharmacy/home.html')

def edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == "POST":
        medicine.name = request.POST.get('name')
        medicine.prescription_required = request.POST.get('prescription_required') == 'on'
        medicine.save()
        return redirect('medicine_list')

    return render(request, 'pharmacy/edit_medicine.html', {
        'medicine': medicine
    })
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    return redirect('medicine_list')
def add_medicine(request):
    if request.method == "POST":
        name = request.POST.get('name')
        prescription_required = request.POST.get('prescription_required') == 'on'

        Medicine.objects.create(
            name=name,
            prescription_required=prescription_required
        )

        return redirect('medicine_list')

    return render(request, 'pharmacy/add_medicine.html')