import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from documents.models import CourierRate


class Command(BaseCommand):
    help = 'Import courier/dispatch rate list from CSV.'

    column_aliases = {
        'description': [
            'description',
            'বিস্তারিত বিবরণ',
        ],
        'quantity': [
            'quantity',
            'পরিমাণ',
        ],
        'amount': [
            'amount',
            'একক মূল্য',
            'টাকা',
            'একক মূল্য / টাকা',
            'একক মূল্য/টাকা',
        ],
        'remarks': [
            'remarks',
            'মন্তব্য',
        ],
    }
    required_columns = ['description', 'amount']
    bangla_digit_translation = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='Path to courier rate CSV file')

    def handle(self, *args, **options):
        csv_path = Path(options['csv_path'])
        if not csv_path.exists():
            raise CommandError(f'CSV file not found: {csv_path}')

        summary = {
            'created': 0,
            'existing': 0,
            'skipped': 0,
            'errors': 0,
        }

        with csv_path.open(newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            column_map = self.get_column_map(reader.fieldnames or [])

            missing = [
                column
                for column in self.required_columns
                if column not in column_map
            ]
            if missing:
                raise CommandError(
                    'CSV is missing required column(s): '
                    + ', '.join(missing)
                )

            for row_number, row in enumerate(reader, start=2):
                cleaned = {
                    key: self.clean_cell(row.get(source_column, ''))
                    for key, source_column in column_map.items()
                }

                if not any(cleaned.values()):
                    summary['skipped'] += 1
                    continue

                description = cleaned.get('description', '')
                quantity = cleaned.get('quantity', '')
                amount_raw = cleaned.get('amount', '')
                remarks = cleaned.get('remarks', '')

                if not description or not amount_raw:
                    summary['errors'] += 1
                    self.stderr.write(
                        f'Row {row_number} skipped: description and amount are required.'
                    )
                    continue

                try:
                    amount = self.parse_amount(amount_raw)
                except (InvalidOperation, ValueError):
                    summary['errors'] += 1
                    self.stderr.write(
                        f'Row {row_number} skipped: invalid amount "{amount_raw}".'
                    )
                    continue

                _, created = CourierRate.objects.get_or_create(
                    description=description,
                    quantity=quantity,
                    amount=amount,
                    defaults={
                        'remarks': remarks,
                        'is_active': True,
                    },
                )

                if created:
                    summary['created'] += 1
                else:
                    summary['existing'] += 1

        self.stdout.write(self.style.SUCCESS('Courier rate import complete.'))
        self.stdout.write(f"Created: {summary['created']}")
        self.stdout.write(f"Existing: {summary['existing']}")
        self.stdout.write(f"Skipped: {summary['skipped']}")
        self.stdout.write(f"Errors: {summary['errors']}")

    def get_column_map(self, fieldnames):
        normalized_headers = {
            self.normalize_header(fieldname): fieldname
            for fieldname in fieldnames
        }
        column_map = {}

        for canonical, aliases in self.column_aliases.items():
            for alias in aliases:
                source_column = normalized_headers.get(self.normalize_header(alias))
                if source_column:
                    column_map[canonical] = source_column
                    break

        return column_map

    def normalize_header(self, value):
        return ' '.join((value or '').strip().casefold().split())

    def clean_cell(self, value):
        return (value or '').strip()

    def parse_amount(self, value):
        cleaned = (
            value.translate(self.bangla_digit_translation)
            .replace(',', '')
            .replace('৳', '')
            .replace('BDT', '')
            .replace('Tk.', '')
            .replace('Tk', '')
            .replace('tk.', '')
            .replace('tk', '')
            .strip()
        )
        amount = Decimal(cleaned)
        if amount < 0:
            raise ValueError('Amount must be zero or positive.')
        return amount
