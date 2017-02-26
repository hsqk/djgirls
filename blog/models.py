from django.db import models
from django.utils import timezone

"""
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
"""

class Seller(models.Model):
    seller_code = models.CharField(max_length = 10, null=True, blank=True)
    matric_no = models.CharField(max_length = 9)
    name = models.CharField(max_length = 200)
    room = models.CharField(max_length = 4)
    #
    mobile = models.CharField(max_length = 8)
    email = models.EmailField()
    #
    qty_in = models.IntegerField(default = 0)
    qty_sold = models.IntegerField(default = 0)
    qty_left = models.IntegerField(default = 0)
    #
    earnings = models.IntegerField(default = 0)
    #
    settled = models.BooleanField(default = False)
    
    def add(self):
        self.save()
    
    def __str__(self):
        return self.name

class Clothes(models.Model):
    item_code = models.CharField(max_length = 100, null=True, blank=True)
    owner = models.ForeignKey(Seller, on_delete = models.CASCADE)
    price = models.IntegerField()
    description = models.CharField(max_length = 200)
    sold = models.BooleanField(default = False)
    recycle = models.BooleanField(default = True)
    
    def add(self):
        self.save()


