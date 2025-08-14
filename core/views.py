from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def tool_truck_calendar(request):
    return render(request, 'core/tool_truck_calendar.html')