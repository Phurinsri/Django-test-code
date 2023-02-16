from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['id', 'slug', 'published', 'created', 'updated']
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['code'].error_messages ={
            'required': 'Please enter book code'
        }
        self.fields['name'].error_messages ={
            'required': 'Please enter book name'
        }
        self.fields['price'].error_messages ={
            'required': 'Please enter book price',
            'invalid': 'Please enter a valid book price'
        }
    def clean(self):
        check_data = super(BookForm,self).clean()
        if not check_data.get('category'):
            self.add_error('category', 'Please select category name')
        if not check_data.get('author'):
            self.add_error('author', 'Please select author name')