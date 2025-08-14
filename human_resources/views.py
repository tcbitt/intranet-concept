from django.shortcuts import render

def hr_home(request):
    return render(request, 'human_resources/hr_home.html')
