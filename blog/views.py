from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Seller, Clothes
from .forms import SellerForm, ClothesForm, SaleForm

# Create your views here.

def seller_list(request):
    sellers = Seller.objects.order_by('name')
    return render(request, 'blog/seller_list.html', {'sellers':sellers})

def clothes_list(request):
    clothes = Clothes.objects.order_by('owner', 'price')
    return render(request, 'blog/clothes_list.html', {'clothes':clothes})


'''
def seller_detail(request, pk):
    seller = get_object_or_404(Seller, pk = pk)
    return render(request, 'blog/seller_detail.html', {'seller':seller})

def clothes_detail(request, pk):
    clothes = get_object_or_404(Clothes, pk = pk)
    return render(request, 'blog/clothes_detail.html', {'clothes':clothes})
'''

import string
alphabet = string.ascii_uppercase
double_letters = []
for i in alphabet:
    for j in alphabet:
        double_letters.append(i+j)

temp = [i for i in zip([i for i in range(0,26)], [i for i in alphabet])]
temp2 = [i for i in zip([i for i in range(26, 702)], double_letters)]
n2l = dict(temp+temp2)


@login_required
def seller_new(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.save()
            newly_added_seller = Seller.objects.get(pk = seller.pk)
            newly_added_seller.seller_code = n2l[seller.pk]
            newly_added_seller.save()
            return redirect('seller_list')
    else:
        form = SellerForm()
    return render(request, 'blog/seller_edit.html', {'form': form})

@login_required
def seller_edit(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    if request.method == "POST":
        form = SellerForm(request.POST, instance=seller)

        if form.is_valid():
            seller = form.save(commit=False)
            seller.save()
            return redirect('seller_list')
    else:
        form = SellerForm(instance=seller)
    return render(request, 'blog/seller_edit.html', {'form': form})


@login_required
def seller_remove(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    seller.delete()
    return redirect('seller_list')



@login_required
def clothes_new(request):
    if request.method == 'POST':
        form = ClothesForm(request.POST)
        if form.is_valid():
            clothes_ini = form.save(commit=False)
            descriptions = clothes_ini.description.split('.')
            for i in range(len(descriptions)):
                clothes = Clothes(owner=clothes_ini.owner, price=clothes_ini.price)
                clothes.description = descriptions[i]
                clothes.save()
                newly_added_clothes = Clothes.objects.get(pk = clothes.pk)
                newly_added_clothes.item_code = clothes.owner.seller_code + str(clothes.pk)
                newly_added_clothes.save()
                clothes.owner.qty_in += 1
                clothes.owner.save()
            return redirect('clothes_list')
    else:
        form = ClothesForm()
    return render(request, 'blog/clothes_edit.html', {'form': form})

@login_required
def clothes_edit(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk)
    if request.method == "POST":
        form = ClothesForm(request.POST, instance=clothes)
    
        if form.is_valid():
            clothes = form.save()
            return redirect('clothes_list')
    else:
        form = ClothesForm()
    return render(request, 'blog/clothes_edit.html', {'form': form})


@login_required
def clothes_remove(request, pk):
    clothes = get_object_or_404(Clothes, pk=pk)
    clothes.delete()
    return redirect('clothes_list')


def sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sales_ini = form.save(commit=False)
            item_code = sales_ini.item_code.split(',')
            for i in range(len(item_code)):
                curr_item = Clothes.objects.get(item_code = item_code[i])
                if curr_item.sold == True:
                    raise Exception('an item is already sold')
            for i in range(len(item_code)):
                curr_item = Clothes.objects.get(item_code = item_code[i])
                curr_item.sold = True
                curr_item.save()
                curr_item.owner.qty_sold += 1
                curr_item.owner.qty_left -= 1
                curr_item.owner.earnings += curr_item.price
                curr_item.owner.save()
            return redirect('clothes_list')
    else:
        form = SaleForm()
    return render(request, 'blog/sale.html', {'form': form})
    
    
    
'''

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

'''
