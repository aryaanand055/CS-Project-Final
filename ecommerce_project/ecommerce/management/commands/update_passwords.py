# yourapp/management/commands/update_passwords.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from ecommerce.models import Customer

class Command(BaseCommand):
    help = 'Update passwords to use a secure hashing algorithm.'
    def handle(self, *args, **options):
        customers = Customer.objects.all()
        for customer in customers:
            # If the password is not hashed, hash it
            if not customer.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
                customer.password = make_password(customer.password)
                customer.save()
                self.stdout.write(self.style.SUCCESS(f'Updated password for {customer.email}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Password for {customer.email} is already hashed'))

        self.stdout.write(self.style.SUCCESS('Passwords update completed.'))
