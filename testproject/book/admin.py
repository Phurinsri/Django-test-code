from django.contrib import admin
from .models import Category, Author, Book, BookComments

class BookCommentStackInline(admin.StackedInline):
    model = BookComments

class BookCommentTabularInline(admin.TabularInline):
    model = BookComments
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'price', 'level', 'published', 'show_image']
    list_filter = ['published']
    search_fields = ['code', 'name']
    prepopulated_fields = {'slug': ['name']}
    fieldsets= (
        (None, {'fields': ['code', 'name', 'slug', 'description','price', 'level', 'image', 'published']}),
        ('Category', {'fields': ['category', 'author'], 'classes':['collapse']}),
    )
    inlines = [ BookCommentTabularInline ]

# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)