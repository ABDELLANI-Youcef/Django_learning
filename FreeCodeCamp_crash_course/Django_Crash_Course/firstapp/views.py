from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from .forms import ReservationForm

# Create your views here.
def hello_world(request):
  return HttpResponse("Hello world")

class HelloAlgeria(View):
  def get(self, request):
    return HttpResponse("Hello Algeria")

def home(request):
  form = ReservationForm()

  if request.method == 'POST':
    form = ReservationForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponse('Success')
  return render(request, 'firstapp/index.html', {'form': form})

