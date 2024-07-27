import pytest
# جلب الكلاس الرئيسيه لانشاء البينات
from tracker.factories import *

# لتحديد انه سوف يتم التعديل علي طريقة الاختبار
@pytest.fixture
# اسم الدالة وسوف نستخدمه في الملف الاخر
def transactions():
  # ارجاع انشاء 20 بيان من ملف البينات الوهميه
  return TransactionFactory.create_batch(20)


# لتحديد انه سوف يتم التعديل علي طريقة الاختبار
@pytest.fixture
# اسم الدالة وسوف نستخدمه في الملف الاخر
def user_transactions():
  # جلب اليوزر من الملف الاخر
  user = UserFactory()
  # انشاء 20 معاملة باستخدام اليوزر
  return TransactionFactory.create_batch(20, user=user)




@pytest.fixture
def user():
  return UserFactory()


@pytest.fixture
# انشاء معاملات باليوزر وارجاع معلومات المعاملات
def transaction_dict_params(user):
  transaction = TransactionFactory.create(user=user)
  return {
    'type':transaction.type,
    'category':transaction.category_id,
    'date': transaction.date,
    'amount':transaction.amount,
  }