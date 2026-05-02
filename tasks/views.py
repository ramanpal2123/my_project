from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


# ── List all tasks ───────────────────────────────────
@login_required
def task_list(request):
    tasks     = Task.objects.filter(user=request.user)
    total     = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending   = tasks.filter(completed=False).count()

    # Filter by priority if requested
    priority = request.GET.get('priority')
    if priority in ['low', 'medium', 'high']:
        tasks = tasks.filter(priority=priority)

    # Filter by status
    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    return render(request, 'tasks/task_list.html', {
        'tasks':     tasks,
        'total':     total,
        'completed': completed,
        'pending':   pending,
    })


# ── Create a task ────────────────────────────────────
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task      = form.save(commit=False)
            task.user = request.user       # assign to logged-in user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


# ── Edit a task ──────────────────────────────────────
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)  # only owner can edit
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Edit'})


# ── Toggle complete/incomplete ───────────────────────
@login_required
def task_toggle(request, pk):
    task           = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    status = 'completed' if task.completed else 'marked as pending'
    messages.success(request, f'Task {status}!')
    return redirect('task_list')


# ── Delete a task ────────────────────────────────────
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})