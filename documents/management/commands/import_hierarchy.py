import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from documents.models import Area, Branch, Division, Region


class Command(BaseCommand):
    help = 'Import division, region, area, and branch hierarchy from CSV.'

    required_columns = ['division', 'region', 'area', 'branch']

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='Path to division_region_area_branch_mapping.csv')

    def handle(self, *args, **options):
        csv_path = Path(options['csv_path'])
        if not csv_path.exists():
            raise CommandError(f'CSV file not found: {csv_path}')

        summary = {
            'divisions_created': 0,
            'regions_created': 0,
            'areas_created': 0,
            'branches_created': 0,
            'skipped_rows': 0,
            'errors': 0,
        }

        with csv_path.open(newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = [field.strip() for field in reader.fieldnames or []]

            if fieldnames != self.required_columns:
                raise CommandError(
                    'CSV columns must be exactly: division, region, area, branch'
                )

            for row_number, row in enumerate(reader, start=2):
                cleaned = {
                    key: (row.get(key) or '').strip()
                    for key in self.required_columns
                }

                if not any(cleaned.values()):
                    summary['skipped_rows'] += 1
                    continue

                missing = [key for key, value in cleaned.items() if not value]
                if missing:
                    summary['errors'] += 1
                    self.stderr.write(
                        f'Row {row_number} skipped: missing {", ".join(missing)}'
                    )
                    continue

                division, created = Division.objects.get_or_create(
                    name=cleaned['division'],
                    defaults={'code': ''},
                )
                if created:
                    summary['divisions_created'] += 1

                region, created = Region.objects.get_or_create(
                    division=division,
                    name=cleaned['region'],
                    defaults={'code': ''},
                )
                if created:
                    summary['regions_created'] += 1

                area, created = Area.objects.get_or_create(
                    region=region,
                    name=cleaned['area'],
                    defaults={'code': ''},
                )
                if created:
                    summary['areas_created'] += 1

                _, created = Branch.objects.get_or_create(
                    area=area,
                    name=cleaned['branch'],
                    defaults={'code': ''},
                )
                if created:
                    summary['branches_created'] += 1

        self.stdout.write(self.style.SUCCESS('Hierarchy import complete.'))
        self.stdout.write(f"Divisions created: {summary['divisions_created']}")
        self.stdout.write(f"Regions created: {summary['regions_created']}")
        self.stdout.write(f"Areas created: {summary['areas_created']}")
        self.stdout.write(f"Branches created: {summary['branches_created']}")
        self.stdout.write(f"Skipped rows: {summary['skipped_rows']}")
        self.stdout.write(f"Errors: {summary['errors']}")
