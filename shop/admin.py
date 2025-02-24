from django.contrib import admin
from django.utils.html import format_html
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    def photo_preview(self, obj):
        return format_html('<img src="{}" style="max-width:128px; max-height:128px; border-radius: 10%"/>'.format(obj.photo.url))
    
    photo_preview.short_description = 'Image'

    list_display = ['photo_preview', 'name', 'price', 'description']

admin.site.register(Product, ProductAdmin)