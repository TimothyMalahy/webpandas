from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            randomness = get_random_string(10)
            username = f"admin{randomness}"
            if not User.objects.filter(
                    username=username,
                    email='admin@example.com').exists():
                print("admin user not found, creating one")
                email = 'admin@example.com'
                new_password = get_random_string(10)

                u = User.objects.create_superuser(username, email, new_password)
                print(f"===================================")
                print(f"A superuser '{username}' was created with email '{email}' and password '{new_password}'")
                print(f"===================================")
            else:
                print("admin user found. Skipping super user creation")
        except Exception as e:
            print(f"There was an error: {e}")