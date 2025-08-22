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
        {'label': getattr(context.get('document'), 'title', 'Untitled Document'), 'url': ''},
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
        *(
            [{'label': context.get('department').name, 'url': reverse_lazy('department-overview')}]
            if context.get('department').name != context.get('current_folder').name else []
        ),
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
        {'label': f"(#{context.get('ticket').id}) - {context.get('ticket').title}", 'url': ''},
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
    # Assets
    'asset-list': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Assets', 'url': ''},
    ],

    'asset-create': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Assets', 'url': reverse_lazy('asset-list')},
        {'label': 'Create Asset', 'url': ''},
    ],

    'asset-dashboard': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Assets', 'url': reverse_lazy('asset-list')},
        {'label': 'Dashboard', 'url': ''},
    ],

    'asset-edit': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Assets', 'url': reverse_lazy('asset-list')},
        {'label': getattr(context.get('asset'), 'name', 'Edit Asset'),
         'url': reverse_lazy('asset-detail', args=[context['asset'].pk])},
        {'label': 'Edit', 'url': ''},
    ],

    'asset-detail': lambda request, context: [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Assets', 'url': reverse_lazy('asset-list')},
        {'label': getattr(context.get('asset'), 'name', f"Asset #{context.get('asset').pk}"), 'url': ''},
    ],

    'no_access': [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': 'Access Denied', 'url': ''},
    ],

}


def auto_breadcrumb(view_name):
    if not view_name:
        return [{'label': 'Home', 'url': reverse_lazy('core:home')}]

    parts = view_name.split(':') if ':' in view_name else [view_name]
    label = parts[-1].replace('-', ' ').replace('_', ' ').title()

    logger.info(f"Auto-generated breadcrumb for view '{view_name}': [{label}]")

    return [
        {'label': 'Home', 'url': reverse_lazy('core:home')},
        {'label': label, 'url': ''},
    ]


# ----------------------BREADCRUMB LOGGER TO FIND MISSING ONES-----------------------
import logging
import os

logger = logging.getLogger('breadcrumbs')
logger.setLevel(logging.INFO)

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'auto_breadcrumbs.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
