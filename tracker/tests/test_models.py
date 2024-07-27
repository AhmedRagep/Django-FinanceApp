import pytest
from tracker.models import Transaction

# لجعل pytest يعرف انه سوف يتعامل مع قاعدة البينات فيقوم بانشاء واحده وهميه
@pytest.mark.django_db
# يجب ان تبدا باسم test_
# تمرير الاسم الموجود في الملف السابق
def test_queryset_get_income_method(transactions):
  # جلب البينات الخاصة ب income
  qs = Transaction.objects.get_income()
  # التاكد من ان البينات موجوده
  assert qs.count() > 0
  # طريقة اخري للتاكد من ان البينات تم انشائها 
  assert all(
    [transaction.type == 'income' for transaction in qs]
  )


# ملحوووظه البينات تكون منشئه وهميا من خلال الامر في الملف السابق


@pytest.mark.django_db
def test_queryset_get_expenses_method(transactions):
  qs = Transaction.objects.get_expenses()
  assert qs.count() > 0
  assert all(
    [transaction.type == 'expense' for transaction in qs]
  )


@pytest.mark.django_db
def test_queryset_get_total_income_method(transactions):
  total_income = Transaction.objects.get_total_income()
  assert total_income == sum(t.amount for t in transactions if t.type == 'income')

  
@pytest.mark.django_db
def test_queryset_get_total_expenses_method(transactions):
  total_expenses = Transaction.objects.get_total_expenses()
  assert total_expenses == sum(t.amount for t in transactions if t.type == 'expense')

