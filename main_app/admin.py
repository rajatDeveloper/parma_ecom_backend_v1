from django.contrib import admin
from main_app.models import Address , Order , Product , User , CartProduct
# Register your models here.

admin.site.register(Address, list_display=['id' , 'address' , 'email' , 'phone'  , 'zipCode'])
admin.site.register(Order, list_display=['id' , 'user' , 'address' , 'total' , 'date' , 'dilveryStatus'])
admin.site.register(Product, list_display=['id' , 'productName' , 'stock' , 'mainPrice' , 'afterDiscountPrice' , 'category' , 'isSale']) , 

admin.site.register(CartProduct, list_display=['id' , 'user' , 'product' ]) , 




