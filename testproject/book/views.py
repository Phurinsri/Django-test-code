from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Book
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger
from .forms import BookForm
from slugify import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
# def index(request):
#     categories = Category.objects.all()
#     books = Book.objects.filter(published= True)

#     categ_id = request.GET.get('category_id')
#     if categ_id:
#         books = books.filter(category_id=categ_id)

#     paginator = Paginator(books, 4)
#     page = request.GET.get('page')
#     try:
#         books = paginator.page(page)
#     except PageNotAnInteger:
#         books = paginator.page(1)
#     except EmptyPage:
#         books = paginator.page(paginator.num_pages)

#     return render(request, 'book/index.html',{
#         'books':books,
#         'categories':categories,
#         'categ_id':categ_id
#     })
from django.views.generic import ListView, DetailView


class BookListView(ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'
    paginate_by = 4

    
    def get_queryset(self):
        return Book.objects.filter(published=True)

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context.update({
            'categories': Category.objects.all()
        })
        return context
        
# def detail(request, slug):
#     book = get_object_or_404(Book, slug=slug)
#     return render(request, 'book/detail.html',{
#         'book':book,
#     })

class BookDetialView(DetailView):
    model = Book
    template_name = 'book\detail.html'
    slug_url_kwarg = 'slug'


def book_add(request):
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.published = True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('book:index', kwargs={}))
        messages.error(request, 'Save Failed!')
    return render(request, 'book/add.html', {
        'form':form,
    })


def card_add(request, slug):
    book = get_object_or_404(Book, slug= slug)
    cart_items = request.session.get('cart_items') or []
    
    # update existing item
    duplicate = False
    for cart in cart_items:
        if cart.get('slug') == book.slug:
            cart['qty'] = int(cart.get('qty') or '1') + 1
            duplicate = True
        
        # not existing item

    if not duplicate:
        cart_items.append({
            'id': book.id,
            'slug': book.slug,
            'name': book.name,
            'price': book.price,
            'qty': 1
        })
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('book:cart_list', kwargs={}))
    
def cart_list(request):
    cart_items = request.session.get('cart_items') or []
    # cart_qty = request.session.get('cart_qty') or 0

    total_qty = 0
    for cart in cart_items:
        total_qty += cart.get('qty')
    
    request.session['cart_qty'] = total_qty
    return render(request, 'book/cart.html', {
        'cart_items': cart_items,
        # 'cart_qty': cart_qty
    })

def card_delete(request, slug):
    cart_items = request.session.get('cart_items') or []
    for index, cart in enumerate(cart_items):
        if cart['slug'] == slug:
            del cart_items[index]
            break
    request.session['cart_items'] = cart_items
    return HttpResponseRedirect(reverse('book:cart_list', kwargs={}))

from django.core.mail import EmailMessage

def cart_checkout(request):
    subject = 'Test Email'
    body = '''
        <p>This is a test new message</p>
    '''
    email = EmailMessage(subject=subject, body=body, from_email='purin36537@gmail.com', to=['xxx@gmail.com'])
    email.content_subtype = 'html'
    email.send()
    return redirect('book:index')


    