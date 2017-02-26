from django import forms

from .models import Seller, Clothes

'''
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
'''

class SellerForm(forms.ModelForm):
    
    class Meta:
        model = Seller
        fields = ('matric_no', 'name', 'room', 'mobile', 'email')

class ClothesForm(forms.ModelForm):
    
    class Meta:
        model = Clothes
        fields = ('owner', 'price', 'description')

class SaleForm(forms.ModelForm):
    
    class Meta:
        model = Clothes
        fields = ('item_code',)

