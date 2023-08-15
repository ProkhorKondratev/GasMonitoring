from django.core.management.base import BaseCommand
from geo_repository.management.commands.legacy_loader import load_oz


class Command(BaseCommand):
    help = 'Загрузка зон из старой БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начата загрузка охранных зон из старой БД'))
        load_oz()

        self.stdout.write(self.style.SUCCESS('Загрузка охранных зон из старой БД успешно завершена'))

