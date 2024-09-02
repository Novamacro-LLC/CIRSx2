from django.shortcuts import render


def home(request):
    title = 'CIRSx: Leading the Way in Treating, Educating, and Serving Those with CIRS.'
    context = {'title': title}
    return render(request, 'index.html', context)

def about(request):
    title = 'About Us'
    context =  {'title': title}
    return render(request, 'about.html', context)

def boty(request):
    title = 'Book of the Year'
    context = {'title': title}
    return render(request, 'book-of-the-year.html', context)

def institute(request):
    title = 'CIRSx Institute'
    context = {'title': title}
    return render(request, 'cirsx-institute.html', context)
