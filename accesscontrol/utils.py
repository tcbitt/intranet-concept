def user_has_role(user, role_name):
    role_hierarchy = {
        'Employee': ['Employee', 'Support', 'Admin'],
        'Support': ['Support', 'Admin'],
        'Admin': ['Admin'],
    }

    allowed_roles = role_hierarchy.get(role_name, [role_name])
    return user.groups.filter(name__in=allowed_roles).exists()

def is_employee(user):
    return user_has_role(user, 'Employee')

def is_support(user):
    return user_has_role(user, 'Support')

def is_admin(user):
    return user_has_role(user, 'Admin')
