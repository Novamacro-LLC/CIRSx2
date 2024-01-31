from django.urls import path, include
from . import views

urlpatterns = [
    path('reference_papers/', views.reference_papers, name='reference_papers'),
    path('bibliographies/', views.bibliographies, name='bibliographies'),
    path('curation/', views.curation, name='curation'),
]
