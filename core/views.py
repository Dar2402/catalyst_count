import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UploadFileForm
from rest_framework import generics, serializers
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .tasks import process_csv, get_progress
from django.http import JsonResponse
from django.conf import settings
import os

# Create your views here.
def home(request):
    return render(request, 'core/home.html')


def progress_view(request):
    file_name = request.GET.get('file')
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    processed_rows, total_rows = get_progress(file_path)
    completed = processed_rows >= (total_rows - 1)
    return JsonResponse({'processed_rows': processed_rows, 'total_rows': total_rows, 'completed': completed})



@login_required
def upload_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = f"{settings.MEDIA_ROOT}/{file.name}"

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            done = process_csv(file_path)

            return JsonResponse({'message': 'File uploaded successfully', 'file_name': file.name, 'done': done})
        else:
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    else: 
        form = UploadFileForm()
        return render(request, 'core/upload_data.html', {'form': form})
    

@login_required
def upload_success(request):
    return render(request, 'core/upload_success.html')

@login_required
def query_builder(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        return render(request, 'core/query_builder.html', {'companies': companies})
    
class CompanyFilterPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class CompanyFilterView(generics.ListAPIView):
    serializer_class = CompanySerializer
    pagination_class = CompanyFilterPagination

    def get_queryset(self):
        filters = Q()
        params = {
            'name': 'name__icontains',
            'domain': 'domain__icontains',
            'year_founded': 'year_founded__icontains',
            'industry': 'industry__icontains',
            'size_range': 'size_range__icontains',
            'locality': 'locality__icontains',
            'country': 'country__icontains',
            'linkedin_url': 'linkedin_url__icontains',
            'employees_count_from': 'current_employee_estimate__gte',
            'employees_count_to': 'current_employee_estimate__lte'
        }

        for param, lookup in params.items():
            value = self.request.query_params.get(param, None)
            if value:
                if param in ['employees_count_from', 'employees_count_to']:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                filters &= Q(**{lookup: value})

        return Company.objects.filter(filters)