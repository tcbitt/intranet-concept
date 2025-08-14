from django.urls import reverse_lazy

from django.urls import reverse_lazy

BREADCRUMB_MAP = {
    # Core
    'core:home': [
        {'label': 'Home', 'url': ''},
    ],
    'core:tool-truck-calendar': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Tool Truck Calendar', 'url': ''},
    ],
    'core:login': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Login', 'url': ''},
    ],
    'core:logout': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Logout', 'url': ''},
    ],

    #  Directory
    'directory-widget': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Directory', 'url': ''},
    ],

    # Documents
    'document-list': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Documents', 'url': ''},
    ],
    'document-detail': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Documents', 'url': reverse_lazy('document-list')},
        {'label': context.get('doc').title, 'url': ''},
    ],
    'department-overview': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Documents', 'url': reverse_lazy('document-list')},
        {'label': 'Departments', 'url': ''},
    ],
    'department-documents': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Documents', 'url': reverse_lazy('document-list')},
        {'label': context.get('department').name, 'url': ''},
    ],
    'folder-view': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Documents', 'url': reverse_lazy('document-list')},
        {'label': context.get('department').name, 'url': reverse_lazy('department-overview')},
        *[
            {'label': ancestor.name, 'url': reverse_lazy('folder-view', args=[context['department'].slug, ancestor.id])}
            for ancestor in context.get('current_folder').get_ancestors()
        ],
        {'label': context.get('current_folder').name, 'url': ''},
    ],

    # Helpdesk
    'ticket_list': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Dashboard', 'url': reverse_lazy('dashboard')},
        {'label': 'All Tickets', 'url': ''},
    ],
    'my_tickets': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Dashboard', 'url': reverse_lazy('dashboard')},
        {'label': 'My Tickets', 'url': ''},
    ],
    'ticket_create': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Dashboard', 'url': reverse_lazy('dashboard')},
        {'label': 'Submit Ticket', 'url': ''},
    ],
    'ticket_detail': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Dashboard', 'url': reverse_lazy('dashboard')},
        {'label': f"Ticket #{context.get('ticket').id}", 'url': ''},
    ],
    'dashboard': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Dashboard', 'url': ''},
    ],
    'no_access': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Access Denied', 'url': ''},
    ],

    # Human Resources
    'hr-home': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'HR Home', 'url': ''},
    ],
}

