from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transaction_list, name='transaction_list'),
    path("create_transaction/", views.create_transaction, name='create_transaction'),
    path("transactions/<int:pk>/update", views.update_transaction, name='update_transaction'),
    path("transactions/<int:pk>/delete", views.delete_transaction, name='delete_transaction'),

    path("get_transactions", views.get_transactions, name='get_transactions'),
]
