import csv
import logging
import os
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor
from .models import Company

logger = logging.getLogger(__name__)

def update_progress(file_path, processed_rows, total_rows):
    print('update_progress got executed')
    progress_file = file_path + '.progress'
    with open(progress_file, 'w') as f:
        f.write(f'{processed_rows},{total_rows}')

def get_progress(file_path):
    progress_file = file_path + '.progress'
    print('get_progress got executed')

    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            processed_rows, total_rows = map(int, f.read().split(','))
            return processed_rows, total_rows
    return 0, 0

def process_csv(file_path, chunk_size=10000):
    print('process_csv got executed')

    """
    Process the CSV file in chunks and utilize parallel processing.
    """
    def process_chunk(chunk, start_row, total_rows):
        """
        Process a chunk of rows and perform bulk create.
        """
        print('provcess_chunk got executed')

        companies = []
        for row in chunk:
            print('row', row)
            locality_parts = row.get('locality', '').split(',')
            if len(locality_parts) == 3:
                city, state, country = tuple(locality_parts)
            else:
                city, state, country = '', '', ''

            companies.append(
                Company(
                    name=row.get('name', ''),
                    domain=row.get('domain', ''),
                    year_founded=row.get('year_founded', ''),
                    industry=row.get('industry', ''),
                    size_range=row.get('size_range', ''),
                    city=city,
                    state=state,
                    locality=row.get('locality', ''),
                    country=country,
                    linkedin_url=row.get('linkedin_url', ''),
                    current_employee_estimate=row.get('current_employee_estimate', ''),
                    total_employee_estimate=row.get('total_employee_estimate', '')
                )
            )
            print(len(companies))
        print(file_path, start_row + len(chunk), total_rows) 
        update_progress(file_path, start_row + len(chunk), total_rows)
        with transaction.atomic():
            Company.objects.bulk_create(companies)

    try:
        total_rows = sum(1 for row in open(file_path, 'r', encoding='utf-8'))
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            chunk = []
            start_row = 0
            with ThreadPoolExecutor() as executor:
                for row in reader:
                    chunk.append(row)
                    if len(chunk) >= chunk_size:
                        executor.submit(process_chunk, chunk, start_row, total_rows)
                        start_row += len(chunk)
                        chunk = []
                
                if chunk:
                    executor.submit(process_chunk, chunk, start_row, total_rows)
            
            executor.shutdown(wait=True)
            return True

    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return False
