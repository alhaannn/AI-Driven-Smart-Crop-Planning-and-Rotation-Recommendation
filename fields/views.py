from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from .models import Field, CropHistory
from .forms import FieldForm, CropHistoryForm


# ============================================
# FIELD VIEWS
# ============================================

def field_list(request):
    """
    Display list of all fields with summary statistics
    """
    fields = Field.objects.all().annotate(
        crop_count=Count('crop_histories')
    )
    
    context = {
        'fields': fields,
        'total_fields': fields.count(),
        'total_acres': fields.aggregate(Sum('size_acres'))['size_acres__sum'] or 0,
    }
    return render(request, 'fields/field_list.html', context)


def field_detail(request, pk):
    """
    Display detailed information about a specific field
    """
    field = get_object_or_404(Field, pk=pk)
    crop_histories = field.crop_histories.all()
    
    # Calculate statistics
    stats = {
        'total_crops': crop_histories.count(),
        'avg_yield': crop_histories.aggregate(Avg('yield_amount'))['yield_amount__avg'] or 0,
        'latest_crop': field.get_latest_crop(),
    }
    
    context = {
        'field': field,
        'crop_histories': crop_histories[:5],  # Show 5 most recent
        'stats': stats,
    }
    return render(request, 'fields/field_detail.html', context)


def field_create(request):
    """
    Create a new field
    """
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.save()
            messages.success(request, f'Field "{field.name}" created successfully!')
            return redirect('field_detail', pk=field.pk)
    else:
        form = FieldForm()
    
    context = {
        'form': form,
        'title': 'Add New Field',
        'button_text': 'Create Field',
    }
    return render(request, 'fields/field_form.html', context)


def field_update(request, pk):
    """
    Update an existing field
    """
    field = get_object_or_404(Field, pk=pk)
    
    if request.method == 'POST':
        form = FieldForm(request.POST, instance=field)
        if form.is_valid():
            field = form.save()
            messages.success(request, f'Field "{field.name}" updated successfully!')
            return redirect('field_detail', pk=field.pk)
    else:
        form = FieldForm(instance=field)
    
    context = {
        'form': form,
        'field': field,
        'title': f'Edit {field.name}',
        'button_text': 'Update Field',
    }
    return render(request, 'fields/field_form.html', context)


def field_delete(request, pk):
    """
    Delete a field
    """
    field = get_object_or_404(Field, pk=pk)
    
    if request.method == 'POST':
        field_name = field.name
        field.delete()
        messages.success(request, f'Field "{field_name}" deleted successfully!')
        return redirect('field_list')
    
    context = {
        'field': field,
    }
    return render(request, 'fields/field_confirm_delete.html', context)


# ============================================
# CROP HISTORY VIEWS
# ============================================

def crop_history_list(request):
    """
    Display list of all crop history records
    """
    crop_histories = CropHistory.objects.select_related('field').all()
    
    # Filter by field if specified
    field_id = request.GET.get('field')
    if field_id:
        crop_histories = crop_histories.filter(field_id=field_id)
    
    context = {
        'crop_histories': crop_histories,
        'fields': Field.objects.all(),
        'selected_field': field_id,
    }
    return render(request, 'fields/crop_history_list.html', context)


def crop_history_detail(request, pk):
    """
    Display detailed information about a specific crop history record
    """
    crop_history = get_object_or_404(CropHistory, pk=pk)
    
    context = {
        'crop_history': crop_history,
        'growing_days': crop_history.get_growing_days(),
        'total_yield': crop_history.get_yield_per_field(),
    }
    return render(request, 'fields/crop_history_detail.html', context)


def crop_history_create(request):
    """
    Create a new crop history record
    """
    if request.method == 'POST':
        form = CropHistoryForm(request.POST)
        if form.is_valid():
            crop_history = form.save()
            messages.success(request, f'Crop history for "{crop_history.crop_name}" added successfully!')
            return redirect('crop_history_detail', pk=crop_history.pk)
    else:
        # Pre-select field if provided in URL
        field_id = request.GET.get('field')
        initial = {'field': field_id} if field_id else {}
        form = CropHistoryForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Add Crop History',
        'button_text': 'Add Record',
    }
    return render(request, 'fields/crop_history_form.html', context)


def crop_history_update(request, pk):
    """
    Update an existing crop history record
    """
    crop_history = get_object_or_404(CropHistory, pk=pk)
    
    if request.method == 'POST':
        form = CropHistoryForm(request.POST, instance=crop_history)
        if form.is_valid():
            crop_history = form.save()
            messages.success(request, f'Crop history updated successfully!')
            return redirect('crop_history_detail', pk=crop_history.pk)
    else:
        form = CropHistoryForm(instance=crop_history)
    
    context = {
        'form': form,
        'crop_history': crop_history,
        'title': f'Edit {crop_history.crop_name} History',
        'button_text': 'Update Record',
    }
    return render(request, 'fields/crop_history_form.html', context)


def crop_history_delete(request, pk):
    """
    Delete a crop history record
    """
    crop_history = get_object_or_404(CropHistory, pk=pk)
    
    if request.method == 'POST':
        crop_name = crop_history.crop_name
        crop_history.delete()
        messages.success(request, f'Crop history for "{crop_name}" deleted successfully!')
        return redirect('crop_history_list')
    
    context = {
        'crop_history': crop_history,
    }
    return render(request, 'fields/crop_history_confirm_delete.html', context)
