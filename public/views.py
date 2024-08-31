from django.shortcuts import render


def home(request):
    title = 'CIRSx: Leading the Way in Treating, Educating, and Serving Those with CIRS.'
    context = {'title': title}
    return render(request, 'index.html', context)
