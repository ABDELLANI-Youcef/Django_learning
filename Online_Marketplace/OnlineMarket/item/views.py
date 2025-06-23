from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.db.models import Q
from .forms import NewItemForm, EditItemForm
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os

def items(request):
  query = request.GET.get('query', '')
  items = Item.objects.filter(is_sold = False)
  category_id = request.GET.get('category_id', 0)
  categories = Category.objects.all()
  if category_id:
    items = items.filter(category_id=category_id)
  if query:
    items = items.filter(Q(name__icontains=query)| Q(description__icontains=query))
  context={
    'items': items,
    'query': query,
    "categories": categories,
    "category_id": int(category_id)
  }
  return render(request, 'item/items.html', context)

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

@receiver(pre_save, sender=Item)
def delete_old_image_on_change(sender, instance, **kwarg):
  if not instance.pk:
    return False
  try:
    old_item = Item.objects.get(pk=instance.pk)
  except Item.DoesNotExist:
    return False
  old_image = old_item.image
  new_image = instance.image
  if old_image and old_image != new_image:
    if os.path.isfile(old_image.path):
      old_image.delete(save=False)
