from django.core.exceptions import PermissionDenied
from .utils import user_has_role

class RoleRequiredMixin:
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not user_has_role(request.user, self.required_role):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
