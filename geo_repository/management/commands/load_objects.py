from django.core.management.base import BaseCommand
from geo_repository.management.commands.legacy_loader import load_objects


class Command(BaseCommand):
    help = 'Загрузка зон из старой БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начата загрузка из старой БД'))
        load_objects()

        self.stdout.write(self.style.SUCCESS('Загрузка из старой БД успешно завершена'))

