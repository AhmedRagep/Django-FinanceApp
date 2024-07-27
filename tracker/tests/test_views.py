from datetime import datetime , timedelta
from django.urls import reverse
import pytest
from tracker.models import *
from pytest_django.asserts import assertTemplateUsed


# لاستخدام قاعدة البينات في الاختبار 
@pytest.mark.django_db
# دالة تأخذ اولا المعاملات اللتي انشئناها في الملف السابق
# ثانيا كائن دجانجو للتعامل مع التطبيق
def test_total_values_appear_on_list_page(user_transactions,client):
  # جلب المستخدم وتسجيل الدخول به
  user = user_transactions[0].user
  client.force_login(user)

  # هذه الأسطر تحسب إجمالي المبالغ للمعاملات
  income_total = sum(t.amount for t in user_transactions if t.type == 'income')
  expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
  net = income_total - expense_total

  # هذا السطر يحصل على استجابة من عرض قائمة المعاملات باستخدام
  # هذا هوا اسم رابط صفحة العرض
  response = client.get(reverse('transaction_list'))

  # للتاكد من ان القيم في الصفحة اللتي ارسلت مع الرابط تساوي القيم اللتي جلبنها
  assert response.context['total_income'] == income_total
  assert response.context['total_expenses'] == expense_total
  assert response.context['net_income'] == net



# لاستخدام قاعدة البينات في الاختبار 
@pytest.mark.django_db
# دالة تأخذ اولا المعاملات اللتي انشئناها في الملف السابق
# ثانيا كائن دجانجو للتعامل مع التطبيق
def test_transaction_type_filter(user_transactions,client):
  # جلب المستخدم وتسجيل الدخول به
  user = user_transactions[0].user
  client.force_login(user)

  # income check
  # جلب نوع البحث والاسم الاول هوا اسم الفلتر والثاني النوع
  # هذا الاسم هوا الموجود في ملف filters.py
  get_params ={'transaction_type':'income'}
  # جلب المعلومات من الفانكشن وتحديد النوع باضافته
  response = client.get(reverse('transaction_list'),get_params)

  # جلب متغير الفلتر من الدالة اللذي يحتوي علي فلترة البيانات
  qs = response.context['filter'].qs

  # حلقة تكرارية علي البينات المفلترة
  for transaction in qs:
    # احتبار البينات نوعها هوا هذا
    assert transaction.type == 'income'


  # expense check
  # نفس السابق
  get_params ={'transaction_type':'expense'}
  response = client.get(reverse('transaction_list'),get_params)

  qs = response.context['filter'].qs

  for transaction in qs:
    assert transaction.type == 'expense'




# لاستخدام قاعدة البينات في الاختبار 
@pytest.mark.django_db
# دالة تأخذ اولا المعاملات اللتي انشئناها في الملف السابق
# ثانيا كائن دجانجو للتعامل مع التطبيق
def test_start_end_date_filter(user_transactions,client):
  # جلب المستخدم وتسجيل الدخول به
  user = user_transactions[0].user
  client.force_login(user)

  # تحديد تاريخ معين للاختبار وهو من 3 اشهر ماضية
  start_date_cutoff = datetime.now().date() - timedelta(days=120)
  # تعريف التاريخ من متغير الدالة الي تاريخ الاختبار
  get_params = {"start_date":start_date_cutoff}
  # جلب المعلومات من الدالة واضافة تعريف التاريخ
  response = client.get(reverse('transaction_list'),get_params)

  # جلب متغير الفلتر
  qs = response.context['filter'].qs
  # حلقة تكرارية علي النتائج
  for transaction in qs:
    # اختبار التاريخ ان يكون اكبر من او يساوي تاريخ الاختبار
    assert transaction.date >= start_date_cutoff


  # تحديد تاريخ معين للاختبار وهو من 20 يوم ماضية
  end_date_cutoff = datetime.now().date() - timedelta(days=20)
  # تعريف التاريخ من متغير الدالة الي تاريخ الاختبار
  get_params = {"end_date":end_date_cutoff}
  # جلب المعلومات من الدالة واضافة تعريف التاريخ
  response = client.get(reverse('transaction_list'),get_params)

  # جلب متغير الفلتر
  qs = response.context['filter'].qs
  # حلقة تكرارية علي النتائج
  for transaction in qs:
    # اختبار التاريخ ان يكون اقل من او يساوي تاريخ الاختبار
    assert transaction.date <= end_date_cutoff


# لاستخدام قاعدة البينات في الاختبار 
@pytest.mark.django_db
# دالة تأخذ اولا المعاملات اللتي انشئناها في الملف السابق
# ثانيا كائن دجانجو للتعامل مع التطبيق
def test_category_filter(user_transactions,client):
  # جلب المستخدم وتسجيل الدخول به
  user = user_transactions[0].user
  client.force_login(user)

  category_pks = Category.objects.all()[:2].values_list('pk', flat=True)

  # تعريف التاريخ من متغير الدالة الي تاريخ الاختبار
  get_params = {"category":category_pks}
  # جلب المعلومات من الدالة واضافة تعريف التاريخ
  response = client.get(reverse('transaction_list'),get_params)

  # جلب متغير الفلتر
  qs = response.context['filter'].qs
  # حلقة تكرارية علي النتائج
  for transaction in qs:
    assert transaction.category.pk in category_pks




@pytest.mark.django_db
def test_add_transaction(user, transaction_dict_params,client):
  # تسجيل الدخول الاجباري
  client.force_login(user)
  # جلب عدد المعاملات
  user_transaction_count = Transaction.objects.filter(user=user).count()

  # اضافة htmx في الهيدر
  headers = {'HTTP_HX-Request':'true'}
  # انشاء معاملة جديدة باستخدام الرابط والمعلومات
  response = client.post(
    reverse('create_transaction'),
    transaction_dict_params,
    **headers
  )

  # التحقق من ان المعاملات زادت بعد انشاء واحد جديد
  assert Transaction.objects.filter(user=user).count() == user_transaction_count + 1

  # التاكد من استخدام هذا القالب في الانشاء
  assertTemplateUsed(response, 'tracker/partials/transaction_success.html')



@pytest.mark.django_db
def test_add_transaction_with_negative_amount(user, transaction_dict_params,client):
  client.force_login(user)
  # جلب عدد المعاملات
  user_transaction_count = Transaction.objects.filter(user=user).count()

  # تعديل السعر بالسالب 
  transaction_dict_params['amount'] = -78

  # انشاء معاملة بالسعر السالب
  response = client.post(
    reverse('create_transaction'),
    transaction_dict_params
  )

  # التاكد انه لم يزيد عدد المعاملات لانه يوجد خطأ
  assert Transaction.objects.filter(user=user).count() == user_transaction_count

  # التاكد من انه ذهب الي صفحة الانشاء مره اخري 
  assertTemplateUsed(response, 'tracker/partials/create_transaction.html')
  # التاكد من انه تم استخدام ارجاع القالب في الهيدر
  assert 'HX-Retarget' in response.headers





@pytest.mark.django_db
def test_update_transaction_with_negative_amount(user, transaction_dict_params,client):
  client.force_login(user)
  assert Transaction.objects.filter(user=user).count() == 1

  transaction = Transaction.objects.first()
  now = datetime.now().date()
  transaction_dict_params['amount'] = 40
  transaction_dict_params['date'] = now
  client.post(
    reverse('update_transaction', kwargs={'pk':transaction.pk}),
    transaction_dict_params
    
  )


  assert Transaction.objects.filter(user=user).count() == 1
  transaction = Transaction.objects.first()
  assert transaction.amount == 40
  assert transaction.date == now




@pytest.mark.django_db
def test_delete_transaction_request(user, transaction_dict_params,client):
  # تسجيل الدخول
  client.force_login(user)
  # الفحص بوجود عملية تم انشاءها
  assert Transaction.objects.filter(user=user).count() == 1
  # جلب العملية
  transaction = Transaction.objects.first()

  # حذف العمليه باستخدام الرابط
  client.delete(
    reverse('delete_transaction', kwargs={'pk':transaction.pk})
  )

  # التاكد انه لا توجد عمليات
  assert Transaction.objects.filter(user=user).count() == 0