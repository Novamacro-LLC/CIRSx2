from django.shortcuts import render
from .models import Document, Curations


def reference_papers(request):
    rsch = Document.objects.filter(doctyp_num=2).order_by('title')
    #rsch = Document.objects
    context = {'rsch': rsch}
    return render(request, 'reference_papers.html', context)


def bibliographies(request):
    bib = Document.objects.filter(doctyp_num=1).order_by('title')
    context = {'bib': bib}
    return render(request, 'bibliographies.html', context)


def curation(request):
    cur = Curations.objects.using('default').values('cat_name').distinct()

    cat = cur.order_by('cat_ordr')
    lst = Document.objects.filter(curr_num__cur_name='Video Curration').order_by('curr_num__cat_ordr')
    context = {'cat': cat, 'lst': lst}
    return render(request, 'curation.html', context)
