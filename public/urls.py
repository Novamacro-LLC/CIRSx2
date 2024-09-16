from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about' ),
    path('book_of_the-year/', views.boty, name='boty'),
    path('conference/', views.conference, name='conference'),
    path('institute/', views.institute, name='institute'),
    path('healers-helpers/', views.healers, name='healers-helpers'),
    path('research-lab/', views.research_lab, name='research-lab'),
    path('shoey-awards/', views.shoey_awards, name='shoey-awards')
]


