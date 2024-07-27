from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.paginator import Paginator
from .models import *
from .filters import *
from .forms import *
from django_htmx.http import retarget


# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')


def transaction_list(request):
    # متغير به الفلتر
    transaction_filter = TransactionFilter(
        # جلب بينات الرابط
        request.GET,
        # جلب جميع البيانات الخاصة اليوزر الحالي للفلترة عليها
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1)

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    context = {
      'transactions':transaction_page,
      'filter':transaction_filter,
      'total_income':total_income,
      'total_expenses':total_expenses,
      'net_income': total_income - total_expenses
    }
    # لو تم استخدام htmx يرسل المعلومات للصفحة دي
    if request.htmx:
      return render(request,'tracker/partials/transaction-container.html',context)
    return render(request,'tracker/transaction-list.html',context)




@login_required
def get_transactions(request):
  page = request.GET.get('page',1)
   # متغير به الفلتر
  transaction_filter = TransactionFilter(
        # جلب بينات الرابط
        request.GET,
        # جلب جميع البيانات الخاصة اليوزر الحالي للفلترة عليها
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

  paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
  context = {
     'transactions':paginator.page(page)
  }
  # لعمل هذه الفانكشن في الجزء المضاف له المتغير
  return render(request,'tracker/partials/transaction-container.html#transaction_list',context)




def create_transaction(request):
    if request.POST:
      form = TransactionForm(request.POST)
      if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        message = 'Transaction was added successfully..'
        return render(request,'tracker/partials/transaction_success.html',{'message':message})
      else:
        response = render(request,'tracker/partials/create_transaction.html',{'form':form})
        return retarget(response,'#transaction-block')

    else:
      form = TransactionForm()
    return render(request,'tracker/partials/create_transaction.html',{'form':form})
       

def update_transaction(request,pk):
    transaction = get_object_or_404(Transaction,id=pk)
    if request.POST:
      form = TransactionForm(request.POST,instance=transaction)
      if form.is_valid():
        transaction = form.save()
        message = 'Transaction was Updated successfully..'
        return render(request,'tracker/partials/transaction_success.html',{'message':message})
      else:
          context = {
            'form':form,
            'transaction':transaction
          }
          response =  render(request,'tracker/partials/update_transaction.html',context)
          return retarget(response,'#transaction-block')
      
    context = {
     'form':TransactionForm(instance=transaction),
     'transaction':transaction
    }
    return render(request,'tracker/partials/update_transaction.html',context)





@login_required
# لتحديد العمليه علي انها للحذف فقط
@require_http_methods(['DELETE'])
def delete_transaction(request,pk):
    transaction = get_object_or_404(Transaction,id=pk,user=request.user)
    transaction.delete()
    context = {
       'message':f'Transaction of {transaction.amount} on {transaction.date} was deleted successfully.'
    }
    return render(request,'tracker/partials/transaction_success.html',context)