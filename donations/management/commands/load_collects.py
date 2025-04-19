from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils.timezone import get_current_timezone as get_cur_tz
from faker import Faker

from donations.models import Collect, Payment

User = get_user_model()
fake = Faker('ru_RU')


class Command(BaseCommand):
    """Скрипт для наполнения БД тестовыми данными."""
    def handle(self, *args, **options):
        for _ in range(100):
            user_data = {
                'username': fake.user_name(),
                'password': fake.password(),
                'email': fake.email(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            user, created = User.objects.get_or_create(**user_data)
            if created:
                user.save()
            collect_data = {
                'owner': User.objects.order_by('?').first(),
                'title': fake.text(20),
                'reason': fake.enum(Collect.Reason),
                'description': fake.text(50),
                'goal_value': fake.random_int(100, 1000000),
                'finish_at': fake.future_datetime(tzinfo=get_cur_tz())
            }
            Collect.objects.create(**collect_data)
            collect = Collect.objects.order_by('?').first()
            payment_data = {
                'collect': collect,
                'total': fake.random_int(1, 100000),
                'payer': User.objects.order_by('?').first()
            }
            Payment.objects.create(**payment_data)

        self.stdout.write('Данные успешно загружены.')
