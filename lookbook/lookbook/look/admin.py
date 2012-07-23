'''
Created on Jun 4, 2012

@author: plin
'''
from lookbook.look.models import Look, Item, LookColor
from django.contrib import admin

class LookAdmin(admin.ModelAdmin):
    fields = ['look_photo', 'look_photo_path', 'look_description','look_photo_upload_IP_addr']

class ItemAdmin(admin.ModelAdmin):
    fields = ['belong_to_look', 'x_position_on_look','y_position_on_look','product_url', 'product_brand', 'product_name', 'item_category']

class LookColorAdmin(admin.ModelAdmin):
    fields = ['belong_to_look', 'red','green','blue', 'hue', 'color_category']


admin.site.register(Look, LookAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(LookColor, LookColorAdmin)