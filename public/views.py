from django.shortcuts import render


def home(request):
    title = 'CIRSx: Leading the Way in Treating, Educating, and Serving Those with CIRS.'
    #Integrate Teachables and CTA
    context = {'title': title}
    return render(request, 'index.html', context)

def about(request):
    title = 'About Us'
    # Add to db and CTA
    context =  {'title': title}
    return render(request, 'about.html', context)

def boty(request):
    title = 'Book of the Year'
    # Add to db and CTA
    context = {'title': title}
    return render(request, 'book-of-the-year.html', context)

def institute(request):
    title = 'CIRSx Institute'
    #Integrate Teachables and CTA
    context = {'title': title}
    return render(request, 'cirsx-institute.html', context)

def conference(request):
    title = 'CIRSX | 2025 Conference Registration'
    # Add details to db and CTA
    context = {'title': title}
    return render(request, 'conference.html', context)

def healers(request):
    title = 'Healers and Helpers'
    # Add to db and CTA
    context = {'title': title}
    return render(request, 'healers-helpers.html', context)
