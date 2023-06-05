import csv
import os

from django.core.management.base import BaseCommand, CommandParser
from recipes.models import Tag


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
                print(row)
                Tag.objects.get_or_create(
                    name=row[0], hex_code=row[1], slug=row[2]
                )
        print(f'Данные из файла "{file_name}" успешно загружены')
