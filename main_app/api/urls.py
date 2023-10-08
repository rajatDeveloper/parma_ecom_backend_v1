from django.urls import path , include 
from .views import data_list , ProductView , ProductGetUpdateDeleteView , AddressListUpdateView , CartProductListCreateView , OrderListCreateView , CartProductDeleteView

urlpatterns = [
        
    path('test/', data_list , name='test'),
    #get all products and add new product to list
    path('products/' ,ProductView.as_view() , name='products' )  , 
    #get single product and update delete 
    path('product/<int:pk>/' , ProductGetUpdateDeleteView.as_view() , name='product') , 
       
    path('users/<int:user_id>/addresses/', AddressListUpdateView.as_view(), name='address-list-update'),    
    
    path('users/<int:user_id>/cart-products/', CartProductListCreateView.as_view(), name='cart-product-list-create'),
    
    path('users/<int:user_id>/orders/', OrderListCreateView.as_view(), name='order-list-create'),
    
    path('cart-products/<int:cart_product_id>/', CartProductDeleteView.as_view(), name='cart-product-delete'),
    
    
 
        
]


