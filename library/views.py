from django.shortcuts import render


def reference_papers(request):
    rsch = Document.objects.filter(doctyp_num=2).order_by('title')
    context = {'rsch': rsch}
    render(request, 'reference_papers.html', context)


def bibliographies(request):
    bib = Document.objects.filter(doctyp_num=1).order_by('title')
    context = {'bib': bib}
    render(request, 'bibliographies.html', context)
