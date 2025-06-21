from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import NewItemForm, EditItemForm
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your views here.
def detail(request, pk):
  item = get_object_or_404(Item, pk=pk)
  related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
  context = {
    'item': item,
    "related_items": related_items
  }
  return render(request, 'item/detail.html', context)

@login_required
def new(request):
  if request.method == 'POST':
    form = NewItemForm(request.POST, request.FILES)

    if form.is_valid():
      item = form.save(commit=False)
      item.created_by = request.user
      item.save()
      return redirect('item:item_detail', pk=item.pk)
  else:
    form = NewItemForm()
  context = {
    'form': form,
    'title': 'New Item'
  }
  return render(request, 'item/form.html', context)

@login_required
def edit(request, pk):
  instance = get_object_or_404(Item, pk=pk)
  if request.method == 'POST':

    form = EditItemForm(request.POST, request.FILES, instance=instance)
    if form.is_valid():
      form.save()
      return redirect('item:item_detail', pk=instance.pk)
  else:
    form = EditItemForm(instance=instance)
  context = {
    'form': form,
    'title': 'Edit Item'
  }

  return render(request, 'item/edit.html', context)

def delete(request, pk):
  item = get_object_or_404(Item, pk=pk)
  item.delete()
  return redirect('dashboard:index')

@receiver(post_delete, sender=Item)
def item_deleted(sender, instance, **kwargs):
  file = instance.image
  if file:
    try:
      file.delete(save=False)
    except Exception as e:
      print(f"Error deleting file: {e}")
  else:
    print("No file to delete.")