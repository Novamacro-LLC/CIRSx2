from django.shortcuts import render
from .models import Document


def reference_papers(request):
    rsch = Document.objects.filter(doctyp_num=2).order_by('title')
    #rsch = Document.objects
    context = {'rsch': rsch}
    return render(request, 'reference_papers.html', context)


def bibliographies(request):
    bib = Document.objects.filter(doctyp_num=1).order_by('title')
    context = {'bib': bib}
    return render(request, 'bibliographies.html', context)
