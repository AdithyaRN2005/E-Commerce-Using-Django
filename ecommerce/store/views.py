from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
# Create your views here.

def category_detail(request,slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)

    return render(request, 'category_detail.html', {
        'category':category,
        'products':products
    })

def product_details(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    return render(request, 'product_details.html', {
        'product':product
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains= query))
    return render(request, 'search.html', {
        'query':query,
        'products':products
    })