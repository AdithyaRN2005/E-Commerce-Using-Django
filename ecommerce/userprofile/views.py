from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from store.forms import ProductForm
from store.models import Product, Category
from django.utils.text import slugify
from django.contrib import messages

def vendor_detail(request, pk):
    user=User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'vendor_detail.html',{
        'user':user,
        'products':products
    })
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = UserProfile.objects.create(user=user)
            return redirect('home')
        # else:
        #     print("Form errors:", form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {
        'form': form
    })

@login_required
def myaccount(request):
    return render(request, 'myaccount.html')

@login_required 
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, 'my_store.html',{
        'products':products
    } )
             
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            slug = slugify(title)
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slug
            product.save()
            messages.success(request, 'The product was added')
            return redirect('my_store')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {
        'form':form,
        'title': 'Add Product'

    })

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    print(request.method)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes was saved')

            return redirect('my_store')


    else:
        form = ProductForm(instance=product) 

    return render(request, 'add_product.html', {
        'title': 'Edit Product',
        'form':form,
        'product': product
    })


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()
    messages.success(request, 'Product was deleted')
    return redirect('my_store')
