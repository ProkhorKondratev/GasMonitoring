from django.core.management.base import BaseCommand
from geo_repository.management.commands.legacy_loader import load_protected


class Command(BaseCommand):
    help = 'Загрузка охраняемых объектов из старой БД'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начата загрузка охраняемых объектов из старой БД'))
        load_protected()

        self.stdout.write(self.style.SUCCESS('Загрузка охраняемых объектов из старой БД успешно завершена'))

