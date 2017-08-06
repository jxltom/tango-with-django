from django.shortcuts import render, get_object_or_404

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    context_dict = {
        'categories': Category.objects.order_by('-likes')[:5],
        'pages': Page.objects.order_by('-views')[:5]
    }
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')


def show_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    pages = Page.objects.filter(category=category)
    context_dict = {'category': category, 'pages': pages}

    return render(request, 'rango/show_category.html', context_dict)


# TODO: Check uniqueness of category
# TODO: No resubmission during refreshing page
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return index(request)

    return render(request, 'rango/add_category.html', {'form': form})


# TODO: No resubmission during refreshing page
def add_page(request, slug):
    category = get_object_or_404(Category, slug=slug)

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return show_category(request, slug)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
