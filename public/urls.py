from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about' ),
    path('book-of-the-year/', views.boty, name='book-of-the-year'),
    path('conference/', views.conference, name='conference'),
    path('cirsx-institute/', views.institute, name='cirsx-institute'),
    path('research-lab/', views.research_lab, name='research-lab'),
    path('shoey-awards/', views.shoey_awards, name='shoey-awards'),
    path('conference-archives/', views.conference_archives, name='conference-archives'),
    path('conference-exhibitors', views.conference_exhibitors, name='conference-exhibitors')
]


