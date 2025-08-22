from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from accesscontrol.decorators import role_required
from accesscontrol.utils import is_employee, is_support, is_admin
from .models import Ticket
from .forms import TicketForm, CommentForm, TicketUpdateForm


@role_required('Support')
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'helpdesk/ticket_list.html', {'tickets': tickets})


@role_required('Employee')
def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'helpdesk/my_tickets.html', {'tickets': tickets})


@role_required('Employee')
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.branch = request.user.userprofile.branch  # Auto-assign branch
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()

    return render(request, 'helpdesk/ticket_form.html', {'form': form})


def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if not is_support(request.user) and ticket.created_by != request.user:
        raise PermissionDenied

    comments = ticket.comments.all()
    comment_form = CommentForm()
    update_form = None

    if is_support(request.user):
        update_form = TicketUpdateForm(instance=ticket)

        if request.method == 'POST' and 'update_ticket' in request.POST:
            update_form = TicketUpdateForm(request.POST, instance=ticket)
            if update_form.is_valid():
                update_form.save()
                return redirect('dashboard')

    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()

    support_users = User.objects.filter(groups__name='Support')

    return render(request, 'helpdesk/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': comment_form,
        'update_form': update_form,
        'support_users': support_users
    })


def dashboard(request):
    user = request.user
    context = {
        'is_support': is_support(user),
        'is_admin': is_admin(user),
        'is_employee': is_employee(user),
    }

    if is_support(user) or is_admin(user):
        context['my_tickets'] = Ticket.objects.filter(assigned_to=user).exclude(status__in=['closed', 'resolved'])
        context['archived_my_tickets'] = Ticket.objects.filter(status__in=['closed', 'resolved'])

        if is_support(user):
            context['unassigned_tickets'] = Ticket.objects.filter(assigned_to__isnull=True, status='open')

        if is_admin(user):
            context['all_tickets'] = Ticket.objects.exclude(status__in=['closed', 'resolved'])
            context['archived_all_tickets'] = Ticket.objects.filter(status__in=['closed', 'resolved'])
            context['user_management'] = True

        status_map = dict(Ticket.STATUS_CHOICES)
        raw_counts = {
            'open': Ticket.objects.filter(status='open', assigned_to__isnull=True).count(),
            'in_progress': Ticket.objects.filter(status='in_progress').count(),
            'resolved': Ticket.objects.filter(status='resolved').count(),
            'closed': Ticket.objects.filter(status='closed').count(),
        }
        context['status_counts_display'] = [
            {'code': code, 'label': status_map.get(code, code.title()), 'count': raw_counts.get(code, 0)}
            for code in ['open', 'in_progress', 'resolved', 'closed']
        ]

    elif is_employee(user):
        context['my_tickets'] = Ticket.objects.filter(created_by=user).exclude(status__in=['closed', 'resolved'])
        context['archived_my_tickets'] = Ticket.objects.filter(created_by=user, status__in=['closed', 'resolved'])

    return render(request, 'helpdesk/dashboard.html', context)


def no_access(request):
    return render(request, 'core/no_access.html')
