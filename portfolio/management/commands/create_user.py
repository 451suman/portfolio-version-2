from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a user for CV data loading'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='suman',
            email='suman@example.com',
            defaults={
                'first_name': 'Suman',
                'last_name': 'Mushyakhwo',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))
