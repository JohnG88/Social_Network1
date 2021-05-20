from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    user = request.user
    hello = 'hello World'

    context = {'hello': hello, 'user': user}
    return render(request, 'main/home.html', context)
    #return HttpResponse('Hello World')