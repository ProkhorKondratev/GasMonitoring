from django.core.management.base import BaseCommand
from geo_repository.management.commands.legacy_loader import load_zones


class Command(BaseCommand):
    help = 'Загрузка зон из старой БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начата загрузка зон минимальных расстояний из старой БД'))
        load_zones()

        self.stdout.write(self.style.SUCCESS('Загрузка зон минимальных расстояний из старой БД успешно завершена'))

