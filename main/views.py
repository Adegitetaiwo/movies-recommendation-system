from django.shortcuts import render

#function will return an Http response to display the index page

def index(request):

    return render(request, 'index.html')
