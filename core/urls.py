from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_data, name='upload_data'),
    path('query/', views.query_builder, name='query_builder'),
    path('upload-success/', views.upload_success, name='upload_success'),
    path('progress/', views.progress_view, name='progress_view'),
    path('api/companies/', views.CompanyFilterView.as_view(), name='company-filter'),
]
