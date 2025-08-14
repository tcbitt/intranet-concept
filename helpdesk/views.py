from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
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
    context = {}

    if is_employee(request.user):
        context['my_tickets'] = Ticket.objects.filter(
            created_by=request.user
        ).exclude(status__in=['closed', 'resolved'])

        context['archived_my_tickets'] = Ticket.objects.filter(
            created_by=request.user,
            status__in=['closed', 'resolved']
        )

    if is_support(request.user) or is_admin(request.user):
        context['my_tickets'] = Ticket.objects.filter(
            assigned_to=request.user
        ).exclude(status__in=['closed', 'resolved'])

        context['archived_my_tickets'] = Ticket.objects.filter(
            models.Q(assigned_to=request.user) | models.Q(created_by=request.user),
            status__in=['closed', 'resolved']
        ).distinct()

    context['unassigned_tickets'] = Ticket.objects.filter(
        assigned_to__isnull=True,
        status='open'
    )

    if is_admin(request.user):
        context['all_tickets'] = Ticket.objects.exclude(status__in=['closed', 'resolved'])
        context['archived_all_tickets'] = Ticket.objects.filter(status__in=['closed', 'resolved'])
        context['user_management'] = True

    if is_support(request.user) or is_admin(request.user):
        context['status_counts'] = {
            'open': Ticket.objects.filter(status='open', assigned_to__isnull=True).count(),
            'in_progress': Ticket.objects.filter(status='in_progress').count(),
            'resolved': Ticket.objects.filter(status='resolved').count(),
            'closed': Ticket.objects.filter(status='closed').count(),
        }

    return render(request, 'helpdesk/dashboard.html', context)

def no_access(request):
    return render(request, 'helpdesk/no_access.html')
