import django_filters
from .models import *
from django import forms


# دالة الفلتر
class TransactionFilter(django_filters.FilterSet):
  transaction_type = django_filters.ChoiceFilter(
    # جلب الاختيارات
    choices=Transaction.TRANSACTION_TYPE,
    # اسم الحقل
    field_name = 'type',
    # لجلب النتيجة بالظبط
    lookup_expr = 'iexact',
    # الافتراضي
    empty_label='any',
  )

  # الفلترة بالتاريخ
  start_date = django_filters.DateFilter(
    # اسم الحقل
    field_name='date',
    # اكبر من او يساوي التاؤيخ المحدد
    lookup_expr='gte',
    # اسم الحقل في العرض
    label='Date From',
    # اضافة انه تاريخ للظهر بشكل جيد في العرض
    widget=forms.DateInput(attrs={'type':'date'})
  )

  # الفلترة بالتاريخ
  end_date = django_filters.DateFilter(
    # اسم الحقل
    field_name='date',
    # اكبر من او يساوي التاؤيخ المحدد
    lookup_expr='lte',
    label='Date To',
    widget=forms.DateInput(attrs={'type':'date'})
  )

  # فلتر العلامات
  # اضافة انه يمكن اختيار اكثر من علامع مع بعض
  category= django_filters.ModelMultipleChoiceFilter(
    # جلب كل العلامات
    queryset=Category.objects.all(),
    # اضافة انه شك بوكس اختار منه اكثر من واحد
    widget=forms.CheckboxSelectMultiple()
  )
  class Meta:
    # اضافة المودل الرئيسيه
    model = Transaction
    # تعريف الاسماء اللتي انشئناها فوق
    fields = ('transaction_type','start_date','end_date','category')
    