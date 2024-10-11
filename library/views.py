from django.shortcuts import render
from django.db import connection
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.core.paginator import Paginator
from .models import Document, PatientHelp, HealersHelpers


def curr_sql():
    sql = 'select lcc.cat_name, ld.title, ld.doc_path from library_document ld left join library_document_cat_num ldcn on ld.id = ldcn.document_id left join library_curationcategory lcc on ldcn.curationcategory_id = lcc.id left join library_curations lc on lcc.cur_num_id = lc.id where lc.id = 1 order by lcc.cat_order'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def resource_library(request):
    title = 'Resource Library'
    q = request.GET.get('q')

    if q:
        vector = SearchVector('title', 'author', 'keywords', 'doc_txt')
        query = SearchQuery(q)
        search_headline = SearchHeadline('doc_txt', query)

        # videos = Video.objects.filter(title__search=q)
        # videos = Video.objects.annotate(search=vector).filter(search=query)
        # videos = Video.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
        doc = Document.objects.annotate(
            rank=SearchRank(vector, query),
            headline=search_headline).filter(
            rank__gte=0.001).filter(doctyp_num=2).order_by('-rank')
        rsch = doc.all()

        p = Paginator(doc, 50)
        page = request.GET.get('page')
        docs = p.get_page(page)

    else:
        rsch = Document.objects.filter(doctyp_num=2).order_by('title')
        docs = None

    context = {'q': q, 'docs': docs, 'rsch': rsch, 'title': title}
    return render(request, 'resource-library.html', context)

def bibliographies(request):
    title = 'Bibliographies'
    q = request.GET.get('q')

    if q:
        vector = SearchVector('title', 'author', 'keywords', 'doc_txt')
        query = SearchQuery(q)
        search_headline = SearchHeadline('doc_txt', query)

        # videos = Video.objects.filter(title__search=q)
        # videos = Video.objects.annotate(search=vector).filter(search=query)
        # videos = Video.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')
        doc = Document.objects.annotate(
            rank=SearchRank(vector, query),
            headline=search_headline).filter(
            rank__gte=0.001).filter(doctyp_num=1).order_by('-rank')
        bib = doc.all()

        p = Paginator(doc, 50)
        page = request.GET.get('page')
        docs = p.get_page(page)

    else:
        bib = Document.objects.filter(doctyp_num=1).order_by('title')
        docs = None

    context = {'q': q, 'docs': docs, 'bib': bib, 'title': title}
    return render(request, 'bibliographies.html', context)

def curation(request):
    lst = curr_sql()
    context = {'lst': lst}
    return render(request, 'curation.html', context)

def video_library(request):
    title = 'Video Library'
    vid = Document.objects.filter(doctyp_num=3).order_by('title')
    context = {'title': title, 'vid': vid}
    return render(request, 'video-library.html', context)

def healers(request):
    title = 'Healers and Helpers'
    # Add CTA
    help = HealersHelpers.objects.all()
    heal = []
    for h in help:
        name = h.name
        doc = Document.objects.filter(id=h.doc_num_id).first()
        link = doc.doc_path.split('/')
        path = 'https://player.vimeo.com/video/'+ link[3] +'?title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"'
        heal.append({'name': name, 'path': path})
    context = {'title': title,  'heal': heal}
    return render(request, 'healers-helpers.html', context)

def patient_resources(request):
    title = 'Patient Resources'
    resource = PatientHelp.objects.all()
    pat = []
    for r in resource:
        name = r.name
        doc = Document.objects.filter(id=r.doc_num_id).first()
        link = doc.doc_path.split('/')
        path = 'https://player.vimeo.com/video/'+ link[3] +'?title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"'
        pat.append({'name': name, 'path': path})
    context = {'title': title, 'pat': pat}
    return render(request, 'patient-resources.html', context)
