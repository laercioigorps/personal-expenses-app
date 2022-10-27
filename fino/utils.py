from django.db.models import Sum
from .models import Transaction


def get_transactions_filter():
    return Transaction.objects.values('date__month', 'date__year').annotate(soma=Sum('total'))


class DateUtils:
    MONTHS = {
        '1': "Janeiro",
        '2': "Fevereiro",
        '3': "Março",
        '4': "Abril",
        '5': "Maio",
        '6': "Junho",
        '7': "Julho",
        '8': "Agosto",
        '9': "Setembro",
        '10': "Outubro",
        '11': "Novembro",
        '12': "Dezembro",
    }
