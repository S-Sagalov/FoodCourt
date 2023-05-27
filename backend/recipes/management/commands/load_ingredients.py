import csv
import os

from django.core.management.base import BaseCommand, CommandParser
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингридиентов из csv файла'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '-f', help='Полный путь к файлу'
        )

    def handle(self, *args, **options):
        file = options.get('f')
        file_name = os.path.basename(file)
        with open(file, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1]
                )
        print(f'Данные из файла "{file_name}" успешно загружены')
