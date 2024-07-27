import random
from django.core.management.base import BaseCommand
from faker import Faker
from tracker.models import *

# لانشاء اوامر الادارة
class Command(BaseCommand):
    # وصف المعاملة
    help = "Generates transactions for testing"

    # دالة لانشاء البينات
    def handle(self, *args, **options):
        # الانشاؤ الوهمي
        fake = Faker()
        # قايمه
        categories = [
            "Bills",
            "Food",
            "Clothes",
            "Medical",
            "Housing",
            "Salary",
            "Social",
            "Transport",
            "Vacation",
        ]

        # تكرار علي القايمة وانشاءها اذا كانت غير موجوده
        for category in categories:
            Category.objects.get_or_create(name=category)

        # get my user
        # جلب اليوزر بهذا الاسم
        user = User.objects.filter(username='ahmed').first()
        # اذا لم يكن موجود
        if not user:
            # انشاء ادمن بالاسم والباس
            user = User.objects.create_superuser(username='ahmed',password='1234')
        # جلب جميع المعلمات
        categories = Category.objects.all()
        # عمل تكرار علي (تايب) 
        types = [x[0] for x in Transaction.TRANSACTION_TYPE]
        # انشاء 20 بيان
        for i in range(20):
            #
            Transaction.objects.create(
                # اختيار معلم عشوائي من المعلمات
                category=random.choice(categories),
                # اليوزر هوا الحالي
                user=user,
                # اختيار رقم عشواءي بين 1 2500
                amount=random.uniform(1, 2500),
                # انشاء تاريخ عشوائي من السنة الماضية الي الان
                date=fake.date_between(start_date='-1y', end_date='today'),
                # اختيار نوع من الانواع عشوائي
                type = random.choice(types)
            )