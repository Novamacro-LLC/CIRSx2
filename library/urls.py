from django.urls import path, include
from . import views

urlpatterns = [
    path('resource-library/', views.resource_library, name='resource-library'),
    path('bibliographies/', views.bibliographies, name='bibliographies'),
    path('curation/', views.curation, name='curation'),
    path('healers-helpers/', views.healers, name='healers-helpers'),
    path('video-library/', views.video_library, name='video-library'),
    path('patient-resources/', views.patient_resources, name='patient-resources')
]
