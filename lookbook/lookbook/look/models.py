from django.db import models
from django.forms import ModelForm
from django.conf import settings

# Create your models here.
class Look(models.Model):
    look_photo = models.ImageField(upload_to='looks')
    look_photo_path = models.FilePathField()
    look_short_desc = models.TextField()
    look_description = models.TextField()
    look_photo_upload_datetime = models.DateTimeField(auto_now=True)
    look_photo_upload_IP_addr = models.IPAddressField()

class LookUploadForm(ModelForm):
    class Meta:
        model = Look
        fields = {'look_photo','look_description'}

class Item(models.Model):
    BRAND_LIST = (
                  ('jcrew','J.Crew'),
                  ('gap','GAP'),
                  ('br','Banana Republic'),
                  ('adidas','adidas')
                 )
    CATEGORY_LIST = (
                     ('top', 'Top'),
                     ('bottom', 'Bottom'),
                     ('dress', 'Dress'),
                     ('bag', 'Bag'),
                     ('shoes', 'Shoes'),
                    )
    belong_to_look = models.ForeignKey('Look')
    x_position_on_look = models.IntegerField()
    y_position_on_look = models.IntegerField()
    product_url = models.URLField()
    product_brand = models.CharField(max_length=20, choices=BRAND_LIST)
    product_name = models.CharField(max_length=100)
    item_category = models.CharField(max_length=20, choices=CATEGORY_LIST)

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = {'product_url','product_brand', 'product_name', 'item_category'}

class LookColor(models.Model):
    COLOR_LIST = (
                  ('r', 'Red'),
                  ('rp', 'Red-Purple'),
                  ('p', 'Purple'),
                  ('pb', 'Purple-Blue'),
                  ('b', 'Blue'),
                  ('bg', 'Blue-Green'),
                  ('g', 'Green'),
                  ('gy', 'Green-Yellow'),
                  ('y', 'Yellow'),
                  ('yr', 'Yellow-Red'),
                  )
    belong_to_look = models.ForeignKey('Look')
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    hue = models.IntegerField(null=True)
    color_category = models.CharField(max_length=20, choices=COLOR_LIST,null=True)
    