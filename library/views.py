from django.shortcuts import render
from django.db import connection
from .models import Document
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.core.paginator import Paginator


def curr_sql():
    sql = 'select lcc.cat_name, ld.title, ld.doc_path from library_document ld left join library_document_cat_num ldcn on ld.id = ldcn.document_id left join library_curationcategory lcc on ldcn.curationcategory_id = lcc.id left join library_curations lc on lcc.cur_num_id = lc.id where lc.id = 1 order by lcc.cat_order'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


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


def curation(request):
    lst = curr_sql()
    context = {'lst': lst}
    return render(request, 'curation.html', context)


def doc_search(request):
    q = request.GET.get('q')

    if q:
        vector = SearchVector('title', 'author', 'keywords', 'doc_txt')
        query = SearchQuery(q)
        search_headline = SearchHeadline('doc_txt', query)

        doc = Document.objects.annotate(
            rank=SearchRank(vector, query),
            headline=search_headline).filter(
            rank__gte=0.001).order_by('-rank')
        docu = doc.all()

        p = Paginator(doc, 10)
        page = request.GET.get('page')
        docs = p.get_page(page)

    else:
        docs = None
        docu = None

    context = {'q': q, 'docs': docs, 'docu': docu}
    return render(request, 'search.html', context)
