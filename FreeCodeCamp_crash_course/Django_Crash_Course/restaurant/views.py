# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingForm
from .models import Menu, Booking



# Create your views here.
def home(request):
    return render(request, 'restaurant/index.html')

def about(request):
    return render(request, 'restaurant/about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    books = Booking.objects.all()
    context = {
        'form':form,
        'books': books
    }
    return render(request, 'restaurant/book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'restaurant/menu.html', {'menu': menu_data})

def display_menu_item(request, pk=None):
    menu_item = None
    if pk:
        menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, 'restaurant/menu_item.html', {'menu_item': menu_item})

def book_detail(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        if '_method' in request.POST and request.POST['_method'] == 'DELETE':
            book.delete()
            return redirect('book')  # Redirect to listing page
    return redirect('book')  # Fallback
