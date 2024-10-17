from django.core.management.base import BaseCommand
from CRM.models import Customer

class Command(BaseCommand):
    help = 'Vaxtı keçmiş feedback qeydlərini təmizləyir'

    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()
        for customer in customers:
            customer.delete_if_expired()
        self.stdout.write(self.style.SUCCESS('Təmizləmə tamamlandı.'))