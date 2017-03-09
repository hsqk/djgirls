from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Seller, Clothes
from .forms import SellerForm, ClothesForm, SaleForm, RefundForm, ReturnForm, RecycleForm, SettlementForm
import re, math

# Create your views here.

def seller_list(request):
    sellers = Seller.objects.order_by('name')
    return render(request, 'blog/seller_list.html', {'sellers':sellers})

def clothes_list(request):
    clothes = Clothes.objects.order_by('owner', 'price')
    return render(request, 'blog/clothes_list.html', {'clothes':clothes})

def event_stats(request):
    clothes = Clothes.objects.all()
    qty_received = len(clothes)
    clothes_sellable = Clothes.objects.all().exclude(price = 0)
    qty_sellable = len(clothes_sellable)
    value = 0
    for i in clothes:
        value += i.price
    clothes_sold = Clothes.objects.filter(sold = True)
    qty_sold = len(clothes_sold)
    sold_value = 0
    for i in clothes_sold:
        sold_value += i.price
    sellers = Seller.objects.all()
    sellers_number = len(sellers)
    shoppers = 'TBA'
    
    avg_ask = round(value/qty_sellable, 2)
    if qty_sold==0:
        avg_bid=0
    else:
        avg_bid = round(sold_value/qty_sold, 2)
    return render(request, 'blog/event_stats.html', {'qty_received': qty_received, 'qty_sellable': qty_sellable, 'value': value, 'qty_sold': qty_sold, 'sold_value': sold_value, 'sellers_number': sellers_number, 'shoppers': shoppers, 'avg_ask': avg_ask, 'avg_bid': avg_bid })


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
            return redirect('clothes_new')
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
                if len(descriptions[i]) < 2:
                    continue
                clothes = Clothes(owner=clothes_ini.owner, price=clothes_ini.price)
                clothes.description = descriptions[i]
                clothes.save()
                newly_added_clothes = Clothes.objects.get(pk = clothes.pk)
                taken_codes = []
                owners_clothes = Clothes.objects.filter(owner = clothes_ini.owner)
                for i in owners_clothes:
                    if i.item_code != None:
                        taken_codes.append(i.item_code)
                taken_numbers = []
                for i in taken_codes:
                    temp_str = ''
                    for j in i:
                        if j in '0123456789':
                            temp_str += j
                    taken_numbers.append(int(temp_str))
                if len(taken_numbers) == 0:
                    newly_added_clothes.item_code = 1
                else:
                    newly_added_clothes.item_code = max(taken_numbers)+1
                newly_added_clothes.item_code = clothes.owner.seller_code + str(newly_added_clothes.item_code)
                newly_added_clothes.save()
                clothes.owner.qty_in += 1
                clothes.owner.save()
            return redirect('clothes_new')
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
    clothes.owner.qty_in -= 1
    clothes.owner.save()
    clothes.delete()
    return redirect('clothes_list')


@login_required
def sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sales_ini = form.save(commit=False)
            temp = sales_ini.item_code.replace(' ', '')
            temp = temp.upper()
            item_code = temp.split(',')
            for i in range(len(item_code)):
                if len(item_code[i]) < 2:
                    continue
                curr_item = Clothes.objects.get(item_code = item_code[i])
                if curr_item.sold == True:
                    raise Exception('an item is already sold')
            
            request.session['transacted_items'] = []
            request.session['total_price'] = 0
            
            for i in range(len(item_code)):
                if len(item_code[i]) < 2:
                    continue
                curr_item = Clothes.objects.get(item_code = item_code[i])
                tempd = {'code': curr_item.item_code, 'description': curr_item.description, 'owner': str(curr_item.owner), 'price': curr_item.price}
                request.session['transacted_items'].append(tempd)
                request.session['total_price'] += curr_item.price
                curr_item.sold = True
                curr_item.save()
                curr_item.owner.qty_sold += 1
                curr_item.owner.qty_left = curr_item.owner.qty_in - curr_item.owner.qty_sold
                curr_item.owner.earnings += curr_item.price
                curr_item.owner.save()
            return redirect('transaction_details')
    else:
        form = SaleForm()
    return render(request, 'blog/sale.html', {'form': form})


@login_required
def refund(request):
    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            refund_ini = form.save(commit=False)
            temp = refund_ini.item_code.replace(' ', '')
            temp = temp.upper()
            item_code = temp.split(',')
            for i in range(len(item_code)):
                if len(item_code[i]) < 2:
                    continue
                curr_item = Clothes.objects.get(item_code = item_code[i])
                if curr_item.sold == False:
                    raise Exception('an item is not even sold yet')

            request.session['transacted_items'] = []
            request.session['total_price'] = 0
            
            for i in range(len(item_code)):
                if len(item_code[i]) < 2:
                    continue
                curr_item = Clothes.objects.get(item_code = item_code[i])
                tempd = {'code': curr_item.item_code, 'description': curr_item.description, 'owner': str(curr_item.owner), 'price': curr_item.price}
                request.session['transacted_items'].append(tempd)
                request.session['total_price'] += curr_item.price
                curr_item.sold = False
                curr_item.save()
                curr_item.owner.qty_sold -= 1
                curr_item.owner.qty_left = curr_item.owner.qty_in - curr_item.owner.qty_sold
                curr_item.owner.earnings -= curr_item.price
                curr_item.owner.save()
            return redirect('transaction_details')
    else:
        form = SaleForm()
    return render(request, 'blog/refund.html', {'form': form})


@login_required
def transaction_details(request):
    if 'transacted_items' in request.session:
        transacted_items = request.session['transacted_items']
        total_price = request.session['total_price']
    return render(request, 'blog/transaction_details.html', {'transacted_items': transacted_items, 'total_price': total_price})


@login_required
def recycle(request):
    if request.method == 'POST':
        form = RecycleForm(request.POST)
        if form.is_valid():
            recycle_ini = form.save(commit=False)
            all_flag = 0
            for i in recycle_ini.item_code:
                if i in '0123456789':
                    break
            else:
                all_flag = 1
            temp = recycle_ini.item_code.replace(' ', '')
            temp = temp.upper()
            if all_flag:
                seller_codes = temp.split(',')
                for s_code in seller_codes:
                    seller = Seller.objects.get(seller_code = s_code)
                    seller_items = Clothes.objects.filter(owner = seller)
                    for i in seller_items:
                        i.recycle = True
                        i.save()
            else:
                item_code = temp.split(',')
                for i in range(len(item_code)):
                    if len(item_code[i]) < 2:
                        continue
                    curr_item = Clothes.objects.get(item_code = item_code[i])
                    curr_item.recycle = True
                    curr_item.save()
            return redirect('recycle')
    else:
        form = RecycleForm()
    return render(request, 'blog/recycle.html', {'form': form})

@login_required
def return_to_owner(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_ini = form.save(commit=False)
            all_flag = 0
            for i in return_ini.item_code:
                if i in '0123456789':
                    break
            else:
                all_flag = 1
            temp = return_ini.item_code.replace(' ', '')
            temp = temp.upper()
            if all_flag:
                seller_codes = temp.split(',')
                for s_code in seller_codes:
                    seller = Seller.objects.get(seller_code = s_code)
                    seller_items = Clothes.objects.filter(owner = seller)
                    for i in seller_items:
                        i.recycle = False
                        i.save()
            else:
                item_code = temp.split(',')
                for i in range(len(item_code)):
                    if len(item_code[i]) < 2:
                        continue
                    curr_item = Clothes.objects.get(item_code = item_code[i])
                    curr_item.recycle = False
                    curr_item.save()
            return redirect('return')
    else:
        form = ReturnForm()
    return render(request, 'blog/return.html', {'form': form})



@login_required
def settlement(request):
    if request.method == 'POST':
        form = SettlementForm(request.POST)
        if form.is_valid():
            settlement_1 = form.save(commit=False)
            seller_code = settlement_1.seller_code.upper()
            seller = Seller.objects.get(seller_code = seller_code)
            seller_name = seller.name
            seller_returns = Clothes.objects.filter(owner = seller, recycle = False, sold = False)
            returns, recycles, sold = dict(), dict(), dict()
            for i in seller_returns:
                returns[i.item_code] = i.description
            seller_payment = seller.earnings
            seller_recycles = Clothes.objects.filter(owner = seller, recycle = True, sold = False)
            for i in seller_recycles:
                recycles[i.item_code] = i.description
            seller_sold = Clothes.objects.filter(owner = seller, sold = True)
            for i in seller_sold:
                sold[i.item_code] = i.description
      
            return render(request, 'blog/settlement_details.html', {'seller_code': seller_code, 'seller_name': seller_name, 'seller_returns': seller_returns, 'seller_payment': seller_payment, 'seller_recycles': seller_recycles, 'seller_sold':seller_sold})
        else:
            return redirect('settlement')
    else:
        form = SettlementForm()
    return render(request, 'blog/settlement.html', {'form': form})

@login_required
def unsettled(request):
    peeps = Seller.objects.filter(settled = False)
    return render(request, 'blog/unsettled.html', {'peeps': peeps})


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
