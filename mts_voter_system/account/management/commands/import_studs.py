import pandas as pd
from django.core.management.base import BaseCommand
from account.models import ApprovedStudent

class Command(BaseCommand):
    help = 'Imports approved student numbers from an Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Ensure the column "Student Number" exists
            if 'Student Number' not in df.columns:
                self.stdout.write(self.style.ERROR('Column "Student Number" not found in the Excel file.'))
                return

            added_count = 0  # Track how many numbers are added
            skipped_count = 0  # Track how many already exist

            # Iterate over the rows and store student numbers in `ApprovedStudent`
            for student_number in df['Student Number'].dropna().astype(str).unique():
                if not ApprovedStudent.objects.filter(student_number=student_number).exists():
                    ApprovedStudent.objects.create(student_number=student_number)
                    added_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Added approved student number: {student_number}'))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f'Student number already exists: {student_number}'))

            self.stdout.write(self.style.SUCCESS(f'Import completed: {added_count} added, {skipped_count} skipped.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
