# import_phones.py
import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from datetime import datetime

class Command(BaseCommand):
    help = 'Import phones from a CSV file into the Phone model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **options):
        with open(options['csv_file_path'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                phone = Phone(
                    id=row['id'],
                    name=row['name'],
                    price=row['price'],
                    image=row['image'],
                    release_date=datetime.strptime(row['release_date'], '%Y-%m-%d').date(),
                    lte_exists=row['lte_exists'] == 'True',
                )
                phone.save()
                self.stdout.write(self.style.SUCCESS(f"Phone '{phone.name}' imported successfully."))