from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string


def widget_view(request):
    query = request.GET.get('search', '').lower()

    dummy_employees = [
        {
            'name': 'Tim ORourke',
            'title': 'IT Director',
            'department': 'Information Technology',
            'email': 'Torourke@irrsupply.com',
            'phone': '555-1234'
        },
        {
            'name': 'Travis Bittner',
            'title': 'Software Engineer',
            'department': 'Engineering',
            'email': 'travis.bittner@irrsupply.com',
            'phone': '555-5678'
        },
        {
            'name': 'Carol Lee',
            'title': 'Marketing Lead',
            'department': 'Marketing',
            'email': 'carol.lee@example.com',
            'phone': '555-9012'
        },
        {
            "name": "Alice Johnson",
            "title": "HR Manager",
            "department": "Human Resources",
            "email": "alice.johnson@example.com",
            "phone": "555-1001"
        },
        {
            "name": "Bob Smith",
            "title": "Sales Executive",
            "department": "Sales",
            "email": "bob.smith@example.com",
            "phone": "555-1002"
        },
        {
            "name": "Carol Lee",
            "title": "Marketing Lead",
            "department": "Marketing",
            "email": "carol.lee@example.com",
            "phone": "555-1003"
        },
        {
            "name": "David Kim",
            "title": "Product Manager",
            "department": "Product",
            "email": "david.kim@example.com",
            "phone": "555-1004"
        },
        {
            "name": "Eva Martinez",
            "title": "UX Designer",
            "department": "Design",
            "email": "eva.martinez@example.com",
            "phone": "555-1005"
        },
        {
            "name": "Frank Nguyen",
            "title": "Software Engineer",
            "department": "Engineering",
            "email": "frank.nguyen@example.com",
            "phone": "555-1006"
        },
        {
            "name": "Grace Patel",
            "title": "Data Analyst",
            "department": "Analytics",
            "email": "grace.patel@example.com",
            "phone": "555-1007"
        },
        {
            "name": "Henry Zhao",
            "title": "IT Support",
            "department": "Information Technology",
            "email": "henry.zhao@example.com",
            "phone": "555-1008"
        },
        {
            "name": "Isabel Torres",
            "title": "Operations Coordinator",
            "department": "Operations",
            "email": "isabel.torres@example.com",
            "phone": "555-1009"
        },
        {
            "name": "Jack Reynolds",
            "title": "Finance Analyst",
            "department": "Finance",
            "email": "jack.reynolds@example.com",
            "phone": "555-1010"
        },
        {
            "name": "Karen Brooks",
            "title": "Legal Advisor",
            "department": "Legal",
            "email": "karen.brooks@example.com",
            "phone": "555-1011"
        },
        {
            "name": "Leo Adams",
            "title": "QA Engineer",
            "department": "Engineering",
            "email": "leo.adams@example.com",
            "phone": "555-1012"
        },
        {
            "name": "Mia Chen",
            "title": "Content Strategist",
            "department": "Marketing",
            "email": "mia.chen@example.com",
            "phone": "555-1013"
        },
        {
            "name": "Noah Davis",
            "title": "Business Analyst",
            "department": "Strategy",
            "email": "noah.davis@example.com",
            "phone": "555-1014"
        },
        {
            "name": "Olivia Green",
            "title": "Customer Success Manager",
            "department": "Customer Success",
            "email": "olivia.green@example.com",
            "phone": "555-1015"
        },
        {
            "name": "Paul Harris",
            "title": "Network Administrator",
            "department": "Information Technology",
            "email": "paul.harris@example.com",
            "phone": "555-1016"
        },
        {
            "name": "Quinn Evans",
            "title": "Recruiter",
            "department": "Human Resources",
            "email": "quinn.evans@example.com",
            "phone": "555-1017"
        },
        {
            "name": "Rachel Scott",
            "title": "Project Manager",
            "department": "Operations",
            "email": "rachel.scott@example.com",
            "phone": "555-1018"
        },
        {
            "name": "Sam Thompson",
            "title": "Security Analyst",
            "department": "Information Security",
            "email": "sam.thompson@example.com",
            "phone": "555-1019"
        },
        {
            "name": "Tina Wallace",
            "title": "Training Specialist",
            "department": "Learning & Development",
            "email": "tina.wallace@example.com",
            "phone": "555-1020"
        }
    ]

    if query:
        employees = [e for e in dummy_employees if query in e['name'].lower() or query in e['department'].lower()]
    else:
        employees = dummy_employees

    employees = sorted(employees, key=lambda e: e['name'].lower())
    paginator = Paginator(employees, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('directory/_widget_results.html', {
            'page_obj': page_obj,
            'search': query
        })
        return JsonResponse({'html': html})

    return render(request, 'directory/widget.html', {
        'page_obj': page_obj,
        'search': query
    })
