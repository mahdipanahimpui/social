from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    
    def get(self, request): # if user come with GET method
        return render(request, 'home/index.html') # point to templates > home > index.html
        
    def post(self, request):
        pass