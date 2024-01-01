from django.shortcuts import render
from .models import Document


def reference_papers(request):
    title = 'Reference Papers'
    rsch = Document.objects.filter(doctyp_num=2).order_by('title')
    context = {'rsch': rsch, 'title': title}
    return render(request, 'reference_papers.html', context)


def bibliographies(request):
    title = 'Bibliographies'
    bib = Document.objects.filter(doctyp_num=1).order_by('title')
    context = {'bib': bib, 'title': title}
    return render(request, 'bibliographies.html', context)
