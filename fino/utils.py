from django.db.models import Sum
from .models import Transaction
def get_transactions_filter():
	return Transaction.objects.values('date__month','date__year').annotate(soma=Sum('total'))