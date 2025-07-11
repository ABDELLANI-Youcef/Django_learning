from django import forms
from .models import Item

INPUT_CLASSES = 'w-full py-4 px-6 rouned-xl border'

class NewItemForm(forms.ModelForm):
  class Meta:
    model = Item
    fields = ('category', 'name', 'description', 'price', 'image')
    widgets = {
      'category': forms.Select(attrs={
        'class': INPUT_CLASSES
      }),
      'name': forms.TextInput(attrs={
        'class': INPUT_CLASSES
      }),
      'description': forms.Textarea(attrs={
        'class': INPUT_CLASSES
      }),
      'price': forms.NumberInput(attrs={
        'class': INPUT_CLASSES
      }),
      'image': forms.FileInput(attrs={
        'class': INPUT_CLASSES
      })
    }

class EditItemForm(forms.ModelForm):
  class Meta:
    model = Item
    fields = ('name', 'description', 'price', 'image', 'is_sold')
    widgets = {
      'name': forms.TextInput(attrs={
        'class': INPUT_CLASSES
      }),
      'description': forms.Textarea(attrs={
        'class': INPUT_CLASSES
      }),
      'price': forms.NumberInput(attrs={
        'class': INPUT_CLASSES
      }),
      'image': forms.FileInput(attrs={
        'class': INPUT_CLASSES
      }),
      'is_sold': forms.CheckboxInput(attrs={
        'class': 'w-4 h-4'
      })
    }