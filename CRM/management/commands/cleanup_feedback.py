from django.core.management.base import BaseCommand
from CRM.models import Customer
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Qeyddən 24 saat sonra müştəriləri təmizləyir'

    def handle(self, *args, **kwargs):
        expired_customers = Customer.objects.filter(
            feedback_checked_time__lte=timezone.now() - timedelta(hours=24)
        )
        expired_customers.update(feedback_checked=False, feedback_checked_time=None)
        self.stdout.write(self.style.SUCCESS('Vaxtı keçmiş müştərilər yeniləndi.'))
