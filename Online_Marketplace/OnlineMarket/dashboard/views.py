from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from item.models import Item, Category

# Create your views here.
@login_required
def index(request):
  items = Item.objects.filter(created_by = request.user)
  categories = Category.objects.all()
  context = {
    'items': items,
    'categories': categories
  }
  return render(request, 'dashboard/index.html', context)